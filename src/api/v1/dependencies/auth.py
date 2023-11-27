from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError

from ..routes.exceptions import Unauthorized
from config.settings import settings


def authenticate(
    creds: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> str:
    try:
        payload = jwt.decode(
            creds.credentials, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
        username: str = payload["email"]
    except (KeyError, AttributeError, JWTError):
        # KeyError: 'email' is not in payload
        # AttributeError: creds.credentials is None
        # JWTError: token is invalid
        raise Unauthorized
    return username
