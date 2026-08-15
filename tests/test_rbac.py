from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.api.dependencies import require_role

USER_CLAIMS = {
    "sub": "957daea0-75ab-4528-8b31-a646ef06b8c4",
    "email": "test@example.com",
    "preferred_username": "test-user",
    "realm_access": {
        "roles": ["user"],
    },
}


def test_user_role_is_allowed():
    dependency = require_role("user")

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="test-token",
    )

    fake_db = Session()

    with (
        patch(
            "backend.app.api.dependencies.get_current_user_claims",
            return_value=USER_CLAIMS,
        ),
        patch(
            "backend.app.api.dependencies.get_or_create_user",
        ) as mock_get_or_create_user,
    ):
        mock_user = mock_get_or_create_user.return_value
        mock_user.is_active = True

        result = dependency(
            credentials=credentials,
            db=fake_db,
        )

    assert result is mock_user
    mock_get_or_create_user.assert_called_once()


def test_admin_role_rejected_for_user():
    dependency = require_role("admin")

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="test-token",
    )

    fake_db = Session()

    with patch(
        "backend.app.api.dependencies.get_current_user_claims",
        return_value=USER_CLAIMS,
    ), pytest.raises(HTTPException) as exc_info:
        dependency(
            credentials=credentials,
            db=fake_db,
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Role 'admin' is required"
