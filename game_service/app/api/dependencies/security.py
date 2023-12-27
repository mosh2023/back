from fastapi import Depends
from fastapi.security import APIKeyHeader
from medsi_fastapi.security import get_current_token

from app.core import config


get_token = get_current_token(config.KEYCLOAK_AUTH_URL)


def internal_api_auth():
    def _internal_api_auth(token=Depends(APIKeyHeader(name="Authorization"))):
        if token == config.API_KEY_TOKEN:
            return token

    if config.AUTH_ENABLED:
        return _internal_api_auth
    return lambda: None
