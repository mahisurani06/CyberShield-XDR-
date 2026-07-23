from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

from app.models.asset import Asset
from app.models.alert import Alert
from app.models.incident import Incident


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_assets = db.query(Asset).count()

    online_assets = db.query(Asset).filter(
        Asset.status == "Online"
    ).count()

    offline_assets = db.query(Asset).filter(
        Asset.status == "Offline"
    ).count()

    total_alerts = db.query(Alert).count()

    new_alerts = db.query(Alert).filter(
        Alert.status == "New"
    ).count()

    investigating_alerts = db.query(Alert).filter(
        Alert.status == "Investigating"
    ).count()

    resolved_alerts = db.query(Alert).filter(
        Alert.status == "Resolved"
    ).count()

    total_incidents = db.query(Incident).count()

    open_incidents = db.query(Incident).filter(
        Incident.status == "Open"
    ).count()

    in_progress_incidents = db.query(Incident).filter(
        Incident.status == "In Progress"
    ).count()

    resolved_incidents = db.query(Incident).filter(
        Incident.status == "Resolved"
    ).count()

    return {
        "assets": {
            "total": total_assets,
            "online": online_assets,
            "offline": offline_assets
        },
        "alerts": {
            "total": total_alerts,
            "new": new_alerts,
            "investigating": investigating_alerts,
            "resolved": resolved_alerts
        },
        "incidents": {
            "total": total_incidents,
            "open": open_incidents,
            "in_progress": in_progress_incidents,
            "resolved": resolved_incidents
        }
    }

@router.get("/severity")
def alert_severity_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    high = db.query(Alert).filter(Alert.severity == "High").count()

    medium = db.query(Alert).filter(Alert.severity == "Medium").count()

    low = db.query(Alert).filter(Alert.severity == "Low").count()

    return {
        "high": high,
        "medium": medium,
        "low": low
    }


@router.get("/incidents/status")
def incident_status_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    open_count = db.query(Incident).filter(
        Incident.status == "Open"
    ).count()

    in_progress = db.query(Incident).filter(
        Incident.status == "In Progress"
    ).count()

    resolved = db.query(Incident).filter(
        Incident.status == "Resolved"
    ).count()

    return {
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved
    }

@router.get("/assets/status")
def asset_status_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    online = db.query(Asset).filter(
        Asset.status == "Online"
    ).count()

    offline = db.query(Asset).filter(
        Asset.status == "Offline"
    ).count()

    return {
        "online": online,
        "offline": offline
    }