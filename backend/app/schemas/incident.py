from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    asset_id: int
    assigned_to: str


class IncidentUpdate(BaseModel):
    title: str
    description: str
    severity: str
    status: str
    assigned_to: str


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    asset_id: int
    assigned_to: str

    class Config:
        from_attributes = True