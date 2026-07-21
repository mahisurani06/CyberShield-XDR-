from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.alert import Alert
from app.models.asset import Asset
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse
from app.auth.oauth2 import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = db.query(Asset).filter(Asset.id == alert.asset_id).first()

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    new_alert = Alert(
        title=alert.title,
        description=alert.description,
        severity=alert.severity,
        asset_id=alert.asset_id
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert

@router.get("/", response_model=list[AlertResponse])
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alerts = db.query(Alert).all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.title = alert_data.title
    alert.description = alert_data.description
    alert.severity = alert_data.severity
    alert.status = alert_data.status

    db.commit()
    db.refresh(alert)

    return alert

@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    db.delete(alert)
    db.commit()

    return {
        "message": "Alert deleted successfully"
    }