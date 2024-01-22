import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core import config
from app.db.repository import AuthRepository
from app.models.api import AuthResponse, Roles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


async def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        auth_payload = payload.get("sub")
        if auth_payload is None:
            raise credentials_exception
        token_data = AuthResponse(**auth_payload)
    except jwt.PyJWTError:
        raise credentials_exception
    auth: AuthRepository = await AuthRepository.get_by_login(token_data.login)
    if auth is None:
        raise credentials_exception
    return auth


async def require_admin(auth: AuthResponse = Depends(verify_token)):
    if auth.role != Roles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return auth


async def require_user(auth: AuthResponse = Depends(verify_token)):
    if auth.role != Roles.user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return auth
