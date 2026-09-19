from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    criticality = Column(String, nullable=False)
    exposure = Column(String, nullable=False)
    patch_status = Column(String, nullable=False)
    owner = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())