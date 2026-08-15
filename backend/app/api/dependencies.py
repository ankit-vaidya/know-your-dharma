import uuid
from collections.abc import Callable
from typing import Any

from backend.app.core.security import (
    bearer_scheme,
    get_current_user_claims,
)
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.services.users import get_or_create_user
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    claims: dict[str, Any] = get_current_user_claims(credentials)

    try:
        keycloak_user_id = uuid.UUID(claims["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identity",
        )

    email = claims.get("email")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email claim is missing",
        )

    display_name = (
        claims.get("name")
        or claims.get("preferred_username")
    )

    user = get_or_create_user(
        db,
        keycloak_user_id=keycloak_user_id,
        email=email,
        display_name=display_name,
    )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user

def require_role(required_role: str) -> Callable:
    def role_dependency(
        credentials: HTTPAuthorizationCredentials | None = Depends(
            bearer_scheme
        ),
        db: Session = Depends(get_db),
    ) -> User:
        claims: dict[str, Any] = get_current_user_claims(credentials)

        try:
            keycloak_user_id = uuid.UUID(claims["sub"])
        except (KeyError, ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user identity",
            )

        realm_access = claims.get("realm_access", {})
        roles = realm_access.get("roles", [])

        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' is required",
            )

        email = claims.get("email")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email claim is missing",
            )

        display_name = (
            claims.get("name")
            or claims.get("preferred_username")
        )

        user = get_or_create_user(
            db,
            keycloak_user_id=keycloak_user_id,
            email=email,
            display_name=display_name,
        )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    return role_dependency