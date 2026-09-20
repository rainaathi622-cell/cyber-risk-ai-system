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
    # Get all vulnerabilities linked to this asset
    vulnerabilities = db.query(Vulnerability).filter(Vulnerability.asset_id == asset.id).all()
    cvss_scores = [v.cvss_score for v in vulnerabilities]

    # Run through yesterday's formula
    result = calculate_asset_risk(
        vulnerabilities=cvss_scores,
        criticality=asset.criticality,
        exposure=asset.exposure,
        patch_status=asset.patch_status
    )

    # Check if a risk score already exists for this asset - if so, update it
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


def get_asset_risk_summaries(db: Session) -> list:
    """
    Get a combined view: asset details + their risk score + vulnerability count.
    This is what the frontend dashboard will actually consume.
    """
    all_assets = db.query(Asset).all()
    summaries = []

    for asset in all_assets:
        risk_score = db.query(RiskScore).filter(RiskScore.asset_id == asset.id).first()
        vuln_count = db.query(Vulnerability).filter(Vulnerability.asset_id == asset.id).count()

        if risk_score:
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

    # Sort by highest risk first - most useful order for a dashboard
    summaries.sort(key=lambda x: x["calculated_score"], reverse=True)

    return summaries