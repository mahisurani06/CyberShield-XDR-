from pydantic import BaseModel


class AlertCreate(BaseModel):
    title: str
    description: str
    severity: str
    asset_id: int


class AlertUpdate(BaseModel):
    title: str
    description: str
    severity: str
    status: str


class AlertResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    asset_id: int

    class Config:
        from_attributes = True