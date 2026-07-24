from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.oauth2 import get_current_user
from app.models.user import User

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
    return result