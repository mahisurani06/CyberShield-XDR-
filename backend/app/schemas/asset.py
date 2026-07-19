from pydantic import BaseModel


class AssetCreate(BaseModel):
    hostname: str
    ip_address: str
    operating_system: str
    asset_type: str
    owner: str


class AssetResponse(BaseModel):
    id: int
    hostname: str
    ip_address: str
    operating_system: str
    asset_type: str
    owner: str
    status: str

    class Config:
        from_attributes = True