from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    criticality: str
    exposure: str
    patch_status: str
    owner: Optional[str] = None


class AssetCreate(BaseModel):
    asset_name: str = Field(..., min_length=2, max_length=100)
    asset_type: Literal["Server", "Database", "Cloud Instance", "Application", "Laptop"]
    criticality: Literal["Critical", "High", "Medium", "Low"]
    exposure: Literal["Public", "Internal", "Restricted"]
    patch_status: Literal["Up-to-date", "Outdated", "Unknown"]
    owner: Optional[str] = Field(None, max_length=100)


class AssetResponse(AssetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True