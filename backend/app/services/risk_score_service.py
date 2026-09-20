from sqlalchemy.orm import Session
from models.asset import Asset
from models.vulnerability import Vulnerability
from models.risk_score import RiskScore
from services.risk_formula import calculate_asset_risk


def calculate_and_save_risk_for_asset(db: Session, asset: Asset) -> RiskScore:
    """
    Calculate risk score for ONE asset based on its linked vulnerabilities,
    then save (or update) the result in the risk_scores table.
    """
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.asset_id == asset.id).all()
    cvss_scores = [v.cvss_score for v in vulnerabilities]

    result = calculate_asset_risk(
        vulnerabilities=cvss_scores,
        criticality=asset.criticality,
        exposure=asset.exposure,
        patch_status=asset.patch_status
    )

    existing_score = db.query(RiskScore).filter(RiskScore.asset_id == asset.id).first()

    if existing_score:
        existing_score.calculated_score = result["score"]
        existing_score.risk_level = result["level"]
        db.commit()
        db.refresh(existing_score)
        return existing_score
    else:
        new_score = RiskScore(
            asset_id=asset.id,
            calculated_score=result["score"],
            risk_level=result["level"]
        )
        db.add(new_score)
        db.commit()
        db.refresh(new_score)
        return new_score


def calculate_risk_for_all_assets(db: Session) -> list:
    """
    Calculate risk scores for EVERY asset in the database.
    Returns a list of RiskScore objects.
    """
    all_assets = db.query(Asset).all()
    results = []

    for asset in all_assets:
        score = calculate_and_save_risk_for_asset(db, asset)
        results.append(score)

    return results


def get_asset_risk_summaries(db: Session, risk_level_filter: str = None) -> list:
    """
    Get a combined view: asset details + their risk score + vulnerability count.
    Optionally filter by risk_level (Critical/High/Medium/Low).
    """
    all_assets = db.query(Asset).all()
    summaries = []

    for asset in all_assets:
        risk_score = db.query(RiskScore).filter(RiskScore.asset_id == asset.id).first()
        vuln_count = db.query(Vulnerability).filter(Vulnerability.asset_id == asset.id).count()

        if risk_score:
            if risk_level_filter and risk_score.risk_level != risk_level_filter:
                continue

            summaries.append({
                "asset_id": asset.id,
                "asset_name": asset.asset_name,
                "asset_type": asset.asset_type,
                "criticality": asset.criticality,
                "exposure": asset.exposure,
                "patch_status": asset.patch_status,
                "calculated_score": risk_score.calculated_score,
                "risk_level": risk_score.risk_level,
                "vulnerability_count": vuln_count
            })

    summaries.sort(key=lambda x: x["calculated_score"], reverse=True)
    return summaries


def get_overall_risk_stats(db: Session) -> dict:
    """
    Get high-level dashboard stats: overall average score, count by level.
    """
    all_summaries = get_asset_risk_summaries(db)

    if not all_summaries:
        return {
            "overall_score": 0,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "total_assets": 0
        }

    total_score = sum(s["calculated_score"] for s in all_summaries)
    overall_score = round(total_score / len(all_summaries), 2)

    return {
        "overall_score": overall_score,
        "critical_count": sum(1 for s in all_summaries if s["risk_level"] == "Critical"),
        "high_count": sum(1 for s in all_summaries if s["risk_level"] == "High"),
        "medium_count": sum(1 for s in all_summaries if s["risk_level"] == "Medium"),
        "low_count": sum(1 for s in all_summaries if s["risk_level"] == "Low"),
        "total_assets": len(all_summaries)
    }