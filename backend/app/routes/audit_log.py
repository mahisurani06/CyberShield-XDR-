from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogResponse

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(AuditLog).all()
    return logs