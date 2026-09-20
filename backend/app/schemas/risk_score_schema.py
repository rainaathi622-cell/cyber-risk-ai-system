from pydantic import BaseModel
from datetime import datetime

class RiskScoreResponse(BaseModel):
    id: int
    asset_id: int
    calculated_score: float
    risk_level: str
    calculated_at: datetime

    class Config:
        from_attributes = True


class AssetRiskSummary(BaseModel):
    asset_id: int
    asset_name: str
    asset_type: str
    criticality: str
    exposure: str
    patch_status: str
    calculated_score: float
    risk_level: str
    vulnerability_count: int