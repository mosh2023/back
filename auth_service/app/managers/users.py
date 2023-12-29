import ormar

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from app.settings import settings
from app.models import User
import jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(login: str, password: str):
    try:
        user = await User.objects.get(login=login)
        if not user.verify_password(password):
            return False
        return user
    except ormar.NoMatch:
        return False


async def get_user_current(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

        user = await User.objects.get(id=user_id)
    except ormar.NoMatch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token.")

    return user
