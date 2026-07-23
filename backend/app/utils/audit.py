from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_email: str,
    action: str,
    module: str,
    details: str
):
    log = AuditLog(
        user_email=user_email,
        action=action,
        module=module,
        details=details
    )

    db.add(log)
    db.commit()