import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core import config
from app.db.repository import AuthRepository, User
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
    user_id = await User.get_by_id(auth.id)

    auth_data = AuthResponse(
        id=auth.id,
        user_id=user_id,
        login=auth.login,
        role=auth.role
    )
    if auth_data is None:
        raise credentials_exception
    return auth_data


async def require_admin(auth: AuthResponse = Depends(verify_token)):
    if auth.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return auth


async def require_user(auth: AuthResponse = Depends(verify_token)):
    if auth.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return auth
