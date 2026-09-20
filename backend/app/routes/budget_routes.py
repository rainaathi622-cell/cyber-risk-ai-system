from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.budget_service import get_budget_recommendations
from schemas.budget_schema import BudgetOptimizationResponse

router = APIRouter(prefix="/budget", tags=["Budget Optimization"])

@router.get("/optimize", response_model=BudgetOptimizationResponse)
def optimize_budget(
    total_budget: float = Query(..., description="Total available budget in rupees", gt=0),
    db: Session = Depends(get_db)
):
    """
    Given a total budget, recommend which vulnerabilities to fix first
    for maximum risk reduction.
    """
    return get_budget_recommendations(db, total_budget)