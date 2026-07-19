from fastapi import APIRouter, Depends

from app.security.roles import admin_required
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(admin_required)
):
    return {
        "message": f"Welcome Admin {current_user.full_name}",
        "role": current_user.role
    }