from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class ThreatLookup(Base):
    __tablename__ = "threat_lookups"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(String, nullable=False)

    ip_address = Column(String, nullable=False)

    risk_level = Column(String, nullable=False)

    risk_score = Column(Integer, nullable=False)

    searched_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )