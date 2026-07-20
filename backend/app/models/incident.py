from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    status = Column(String, default="Open")

    asset_id = Column(Integer, ForeignKey("assets.id"))

    assigned_to = Column(String, nullable=False)

    asset = relationship("Asset")