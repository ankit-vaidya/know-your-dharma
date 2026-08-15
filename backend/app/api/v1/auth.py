from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    user: User = Depends(get_current_user),
) -> dict:
    return {
        "id": str(user.id),
        "keycloak_user_id": str(user.keycloak_user_id),
        "email": user.email,
        "display_name": user.display_name,
        "is_active": user.is_active,
    }