from sqlalchemy.orm import Session
from models.asset import Asset
from models.vulnerability import Vulnerability
from models.risk_score import RiskScore
from services.budget_formula import build_fix_recommendations, optimize_budget_allocation


def get_all_vulnerabilities_with_context(db: Session) -> list:
    """
    Pull every vulnerability from the database, joined with its asset's details
    and current risk score, formatted for the budget formula.
    """
    vulnerabilities = db.query(Vulnerability).all()
    enriched_list = []

    for vuln in vulnerabilities:
        asset = db.query(Asset).filter(Asset.id == vuln.asset_id).first()
        if not asset:
            continue

        risk_score_record = db.query(RiskScore).filter(RiskScore.asset_id == asset.id).first()
        current_risk_score = risk_score_record.calculated_score if risk_score_record else 0

        enriched_list.append({
            "vuln_id": vuln.id,
            "cve_id": vuln.cve_id,
            "asset_id": asset.id,
            "asset_name": asset.asset_name,
            "asset_type": asset.asset_type,
            "criticality": asset.criticality,
            "exposure": asset.exposure,
            "patch_status": asset.patch_status,
            "cvss_score": vuln.cvss_score,
            "current_risk_score": current_risk_score
        })

    return enriched_list


def get_budget_recommendations(db: Session, total_budget: float) -> dict:
    """
    Main function: get all vulnerabilities with context, build recommendations,
    and run the budget optimization algorithm.
    """
    vulnerabilities_with_context = get_all_vulnerabilities_with_context(db)

    if not vulnerabilities_with_context:
        return {
            "selected_fixes": [],
            "total_cost": 0,
            "total_risk_reduction": 0,
            "remaining_budget": total_budget,
            "skipped_fixes": [],
            "total_budget": total_budget
        }

    recommendations = build_fix_recommendations(vulnerabilities_with_context)
    result = optimize_budget_allocation(recommendations, total_budget)

    return result