import getpass
import sys

import requests

# Usage:  python scripts/smoke_test.py            (tests your local backend)
#         python scripts/smoke_test.py https://your-deployed-backend-address
BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = 40

results = []


def check(name, passed, detail=""):
    results.append(bool(passed))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}" + (f"  ({detail})" if detail else ""))


def info(name, detail):
    print(f"[INFO] {name}  ({detail})")


def finish():
    passed = sum(results)
    total = len(results)
    print(f"\n{passed} of {total} checks passed.")
    if passed != total:
        print("Look at the FAIL lines above to see which step is still missing.")
    sys.exit(0 if passed == total else 1)


def main():
    print(f"Testing backend at {BASE_URL}\n")

    # ---- 1. Backend and database ----
    try:
        r = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
    except requests.RequestException as error:
        check("Backend reachable", False, str(error))
        finish()
    check("Backend reachable", r.status_code == 200, f"status {r.status_code}")

    r = requests.get(f"{BASE_URL}/test-db", timeout=TIMEOUT)
    connected = r.status_code == 200 and r.json().get("database") == "Connected successfully"
    check("Database connected", connected)

    # ---- 2. Login protection ----
    r = requests.get(f"{BASE_URL}/assets/", timeout=TIMEOUT)
    check("Assets blocked without login", r.status_code == 401, f"status {r.status_code}")

    r = requests.get(
        f"{BASE_URL}/assets/",
        headers={"Authorization": "Bearer abc.def.ghi"},
        timeout=TIMEOUT,
    )
    check("Fake login token rejected", r.status_code == 401, f"status {r.status_code}")

    email = input("Login email: ").strip()
    password = getpass.getpass("Login password (hidden): ")
    r = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=TIMEOUT,
    )
    check("Login works", r.status_code == 200, f"status {r.status_code}")
    if r.status_code != 200:
        finish()
    headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

    # ---- 3. Assets and risk scores ----
    r = requests.get(f"{BASE_URL}/assets/", headers=headers, timeout=TIMEOUT)
    assets_ok = r.status_code == 200 and isinstance(r.json(), list)
    asset_count = len(r.json()) if assets_ok else 0
    check("Assets list loads", assets_ok, f"{asset_count} assets")

    r = requests.get(f"{BASE_URL}/risk-scores/", headers=headers, timeout=TIMEOUT)
    scores_ok = r.status_code == 200
    summaries = r.json() if scores_ok else []
    check("Risk scores load", scores_ok, f"{len(summaries)} scored assets")

    scores = [s["calculated_score"] for s in summaries]
    check("Risk list sorted highest first", scores == sorted(scores, reverse=True))
    check("All scores are between 0 and 100", all(0 <= s <= 100 for s in scores))
    check(
        "Every asset has a score",
        len(summaries) == asset_count,
        f"{len(summaries)} scored / {asset_count} assets",
    )

    r = requests.get(f"{BASE_URL}/risk-scores/stats", headers=headers, timeout=TIMEOUT)
    stats = r.json() if r.status_code == 200 else {}
    level_total = sum(
        stats.get(key, 0)
        for key in ("critical_count", "high_count", "medium_count", "low_count")
    )
    check(
        "Dashboard numbers add up",
        r.status_code == 200 and level_total == stats.get("total_assets"),
        f"levels add up to {level_total}, total {stats.get('total_assets')}",
    )

    timed = requests.get(f"{BASE_URL}/risk-scores/", headers=headers, timeout=TIMEOUT)
    total_ms = timed.elapsed.total_seconds() * 1000
    server_ms = timed.headers.get("X-Process-Time-ms", "not available")
    info("GET /risk-scores/ speed", f"{total_ms:.0f} ms total, server reports {server_ms} ms")

    # ---- 4. Budget recommendations ----
    r = requests.get(
        f"{BASE_URL}/budget/optimize",
        params={"total_budget": 50000},
        headers=headers,
        timeout=TIMEOUT,
    )
    budget_ok = r.status_code == 200
    check("Budget recommendation loads", budget_ok, f"status {r.status_code}")
    if budget_ok:
        data = r.json()
        check("Budget is never exceeded", data["total_cost"] <= 50000.01)
        check(
            "Remaining budget adds up",
            abs(data["remaining_budget"] - (50000 - data["total_cost"])) < 0.05,
        )

    for bad_value in (0, -500, 999999999999):
        r = requests.get(
            f"{BASE_URL}/budget/optimize",
            params={"total_budget": bad_value},
            headers=headers,
            timeout=TIMEOUT,
        )
        check(f"Budget {bad_value} rejected", r.status_code == 422, f"status {r.status_code}")

    # ---- 5. Asset checks ----
    placeholder = {
        "asset_name": "string",
        "asset_type": "string",
        "criticality": "string",
        "exposure": "string",
        "patch_status": "string",
        "owner": "string",
    }
    r = requests.post(f"{BASE_URL}/assets/", json=placeholder, headers=headers, timeout=TIMEOUT)
    check("Placeholder asset values rejected", r.status_code == 422, f"status {r.status_code}")
    if r.status_code == 200:
        # The junk row was saved, so remove it again
        requests.delete(f"{BASE_URL}/assets/{r.json()['id']}", headers=headers, timeout=TIMEOUT)

    good_asset = {
        "asset_name": "Smoke Test Asset",
        "asset_type": "Server",
        "criticality": "Low",
        "exposure": "Restricted",
        "patch_status": "Up-to-date",
        "owner": "QA",
    }
    r = requests.post(f"{BASE_URL}/assets/", json=good_asset, headers=headers, timeout=TIMEOUT)
    created = r.status_code == 200
    check("Valid asset can be created", created, f"status {r.status_code}")

    if created:
        asset_id = r.json()["id"]
        try:
            r = requests.get(f"{BASE_URL}/risk-scores/", headers=headers, timeout=TIMEOUT)
            ids = [s["asset_id"] for s in r.json()] if r.status_code == 200 else []
            check("New asset appears in the risk list right away", asset_id in ids)
        finally:
            r = requests.delete(f"{BASE_URL}/assets/{asset_id}", headers=headers, timeout=TIMEOUT)
            check("Test asset deleted without error", r.status_code == 200, f"status {r.status_code}")

        r = requests.get(f"{BASE_URL}/assets/{asset_id}", headers=headers, timeout=TIMEOUT)
        check("Deleted asset is really gone", r.status_code == 404, f"status {r.status_code}")

    finish()


if __name__ == "__main__":
    main()