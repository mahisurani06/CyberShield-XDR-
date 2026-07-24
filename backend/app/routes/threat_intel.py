from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User
from app.models.threat_lookup import ThreatLookup
from app.utils.audit import create_audit_log
from app.schemas.threat_intel import IPLookupRequest
from app.services.abuseipdb import check_ip

router = APIRouter(
    prefix="/threat-intel",
    tags=["Threat Intelligence"]
)

@router.post("/ip-check")
def ip_lookup(
    request: IPLookupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = check_ip(request.ip_address)

    lookup = ThreatLookup(
        user_email=current_user.email,
        ip_address=result["ip_address"],
        risk_level=result["risk_level"],
        risk_score=result["risk_score"]
    )

    db.add(lookup)
    db.commit()

    create_audit_log(
    db=db,
    user_email=current_user.email,
    action="LOOKUP",
    module="Threat Intelligence",
    details=f"Checked IP {request.ip_address}"
)

    return result
