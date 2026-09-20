import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from database import SessionLocal, engine, Base
from models import asset, vulnerability, risk_score
from services.risk_score_service import calculate_risk_for_all_assets, get_asset_risk_summaries

# Make sure all tables exist (including the new risk_scores table)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    print("Calculating risk scores for all assets...")
    results = calculate_risk_for_all_assets(db)
    print(f"Calculated risk scores for {len(results)} assets.\n")

    print("=== Risk Summary (Highest Risk First) ===")
    summaries = get_asset_risk_summaries(db)
    for s in summaries:
        print(f"{s['asset_name']:<35} | Score: {s['calculated_score']:>6} | Level: {s['risk_level']:<8} | Vulns: {s['vulnerability_count']}")

finally:
    db.close()