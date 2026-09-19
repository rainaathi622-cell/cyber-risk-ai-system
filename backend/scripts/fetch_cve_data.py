import os
import sys
import requests
from dotenv import load_dotenv

# Add the app folder to the path so we can import database and models
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from database import SessionLocal, engine, Base
from models.asset import Asset
from models.vulnerability import Vulnerability

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

NVD_API_KEY = os.getenv("NVD_API_KEY")
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_critical_cves(results_limit=20):
    """Fetch recent CRITICAL severity CVEs from NVD"""
    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    params = {
        "cvssV3Severity": "CRITICAL",
        "resultsPerPage": results_limit
    }

    print("Fetching CVE data from NVD...")
    response = requests.get(NVD_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    vulnerabilities = data.get("vulnerabilities", [])
    print(f"Fetched {len(vulnerabilities)} CVEs successfully.")
    return vulnerabilities


def extract_cve_info(cve_item):
    """Extract the fields we need from a raw NVD CVE item"""
    cve = cve_item.get("cve", {})
    cve_id = cve.get("id", "UNKNOWN")

    description = ""
    for desc in cve.get("descriptions", []):
        if desc.get("lang") == "en":
            description = desc.get("value", "")
            break

    cvss_score = 0.0
    metrics = cve.get("metrics", {})
    if "cvssMetricV31" in metrics:
        cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
    elif "cvssMetricV30" in metrics:
        cvss_score = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]

    return {
        "cve_id": cve_id,
        "description": description[:500],
        "cvss_score": cvss_score
    }


def create_mock_assets(db):
    """Create a realistic set of mock organization assets"""
    mock_assets = [
        {"asset_name": "Web Server 01", "asset_type": "Server", "criticality": "Critical", "exposure": "Public", "patch_status": "Outdated", "owner": "IT Infrastructure"},
        {"asset_name": "Web Server 02", "asset_type": "Server", "criticality": "High", "exposure": "Public", "patch_status": "Up-to-date", "owner": "IT Infrastructure"},
        {"asset_name": "Internal File Server", "asset_type": "Server", "criticality": "High", "exposure": "Internal", "patch_status": "Outdated", "owner": "IT Infrastructure"},
        {"asset_name": "HR Database", "asset_type": "Database", "criticality": "Critical", "exposure": "Restricted", "patch_status": "Up-to-date", "owner": "HR Department"},
        {"asset_name": "Customer CRM Cloud Instance", "asset_type": "Cloud Instance", "criticality": "Critical", "exposure": "Public", "patch_status": "Outdated", "owner": "Sales Team"},
        {"asset_name": "Employee Laptop - Finance01", "asset_type": "Laptop", "criticality": "Medium", "exposure": "Internal", "patch_status": "Outdated", "owner": "Finance Team"},
        {"asset_name": "Employee Laptop - Dev03", "asset_type": "Laptop", "criticality": "Medium", "exposure": "Internal", "patch_status": "Up-to-date", "owner": "Engineering Team"},
        {"asset_name": "Payment Gateway API", "asset_type": "Application", "criticality": "Critical", "exposure": "Public", "patch_status": "Up-to-date", "owner": "Engineering Team"},
        {"asset_name": "Internal Wiki App", "asset_type": "Application", "criticality": "Low", "exposure": "Internal", "patch_status": "Outdated", "owner": "Engineering Team"},
        {"asset_name": "Backup Storage Server", "asset_type": "Server", "criticality": "High", "exposure": "Restricted", "patch_status": "Unknown", "owner": "IT Infrastructure"},
    ]

    created_assets = []
    for asset_data in mock_assets:
        existing = db.query(Asset).filter(Asset.asset_name == asset_data["asset_name"]).first()
        if existing:
            created_assets.append(existing)
            continue
        asset = Asset(**asset_data)
        db.add(asset)
        db.commit()
        db.refresh(asset)
        created_assets.append(asset)

    print(f"Created/verified {len(created_assets)} mock assets.")
    return created_assets


def link_cves_to_assets(db, cve_list, assets):
    """Randomly but sensibly link fetched CVEs to mock assets"""
    import random

    for i, cve_item in enumerate(cve_list):
        cve_info = extract_cve_info(cve_item)

        if not cve_info["cve_id"] or cve_info["cve_id"] == "UNKNOWN":
            continue

        existing = db.query(Vulnerability).filter(Vulnerability.cve_id == cve_info["cve_id"]).first()
        if existing:
            continue

        asset = random.choice(assets)

        vuln = Vulnerability(
            cve_id=cve_info["cve_id"],
            asset_id=asset.id,
            cvss_score=cve_info["cvss_score"],
            description=cve_info["description"]
        )
        db.add(vuln)

    db.commit()
    print("Linked CVEs to assets successfully.")


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        assets = create_mock_assets(db)
        cve_list = fetch_critical_cves(results_limit=20)
        if cve_list:
            link_cves_to_assets(db, cve_list, assets)
        else:
            print("No CVE data fetched. Check your API key or internet connection.")
    finally:
        db.close()


if __name__ == "__main__":
    main()