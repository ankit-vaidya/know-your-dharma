import uuid

from backend.app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_user(
    db: Session,
    *,
    keycloak_user_id: uuid.UUID,
    email: str,
    display_name: str | None,
) -> User:
    user = db.scalar(
        select(User).where(
            User.keycloak_user_id == keycloak_user_id
        )
    )

    if user is not None:
        return user

    user = User(
        keycloak_user_id=keycloak_user_id,
        email=email,
        display_name=display_name,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user