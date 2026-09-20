from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    calculated_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())