from fastapi import APIRouter, Depends

from app.auth.dependencies import require_role
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/hod",
    tags=["HOD"],
)


@router.get("/protected")
def hod_protected_route(
    current_user: User = Depends(
        require_role("HOD")
    ),
):
    return {
        "message": "HOD access granted",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }