from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.incident import Incident
from app.models.asset import Asset
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse
)
from app.auth.oauth2 import get_current_user
from app.security.roles import analyst_required, admin_required

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(analyst_required)
):
    asset = db.query(Asset).filter(
        Asset.id == incident.asset_id
    ).first()

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    new_incident = Incident(
        title=incident.title,
        description=incident.description,
        severity=incident.severity,
        asset_id=incident.asset_id,
        assigned_to=incident.assigned_to
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Incident).all()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    updated: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(analyst_required)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.title = updated.title
    incident.description = updated.description
    incident.severity = updated.severity
    incident.status = updated.status
    incident.assigned_to = updated.assigned_to

    db.commit()
    db.refresh(incident)

    return incident


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return {
        "message": "Incident deleted successfully"
    }