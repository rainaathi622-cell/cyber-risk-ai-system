from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from services.risk_score_service import (
    calculate_risk_for_all_assets,
    get_asset_risk_summaries,
    get_overall_risk_stats
)
from schemas.risk_score_schema import AssetRiskSummary, OverallRiskStats

router = APIRouter(prefix="/risk-scores", tags=["Risk Scores"])

@router.post("/calculate")
def trigger_risk_calculation(db: Session = Depends(get_db)):
    """Manually trigger risk score calculation for all assets"""
    results = calculate_risk_for_all_assets(db)
    return {"message": f"Calculated risk scores for {len(results)} assets"}

@router.get("/", response_model=List[AssetRiskSummary])
def get_all_risk_summaries(
    risk_level: Optional[str] = Query(None, description="Filter by Critical, High, Medium, or Low"),
    db: Session = Depends(get_db)
):
    """Get all assets with their risk scores, sorted highest risk first. Optional filter by risk_level."""
    return get_asset_risk_summaries(db, risk_level_filter=risk_level)

@router.get("/stats", response_model=OverallRiskStats)
def get_risk_stats(db: Session = Depends(get_db)):
    """Get dashboard summary stats: overall score and counts by risk level"""
    return get_overall_risk_stats(db)