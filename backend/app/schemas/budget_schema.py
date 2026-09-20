from pydantic import BaseModel
from typing import List


class FixRecommendation(BaseModel):
    vuln_id: int
    cve_id: str
    asset_id: int
    asset_name: str
    asset_type: str
    criticality: str
    exposure: str
    patch_status: str
    cvss_score: float
    current_risk_score: float
    estimated_cost: float
    risk_reduction: float
    priority_ratio: float


class BudgetOptimizationResponse(BaseModel):
    selected_fixes: List[FixRecommendation]
    total_cost: float
    total_risk_reduction: float
    remaining_budget: float
    skipped_fixes: List[FixRecommendation]
    total_budget: float