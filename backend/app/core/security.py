from typing import Any

import jwt
from backend.app.core.config import get_settings
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_token(
    credentials: HTTPAuthorizationCredentials | None,
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()

    try:
        jwks_client = PyJWKClient(
            settings.keycloak_jwks_url,
        )

        signing_key = jwks_client.get_signing_key_from_jwt(
            token,
        )

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.keycloak_client_id,
            issuer=settings.keycloak_issuer,
            options={
                "require": [
                    "exp",
                    "iat",
                    "iss",
                    "sub",
                    "aud",
                ],
            },
        )

        return claims

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_claims(
    credentials: HTTPAuthorizationCredentials | None,
) -> dict[str, Any]:
    token = get_current_token(credentials)

    return decode_access_token(token)