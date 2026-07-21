from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    status = Column(String, default="New")

    asset_id = Column(Integer, ForeignKey("assets.id"))

    asset = relationship("Asset")