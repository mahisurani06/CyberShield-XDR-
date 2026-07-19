from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    hostname = Column(String, nullable=False)

    ip_address = Column(String, unique=True, nullable=False)

    operating_system = Column(String, nullable=False)

    asset_type = Column(String, nullable=False)

    owner = Column(String, nullable=False)

    status = Column(String, default="Online")