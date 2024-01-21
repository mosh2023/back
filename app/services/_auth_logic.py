import bcrypt
from datetime import datetime, timedelta
from ..db.repository.auth import AuthRepository

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# SECRET_KEY = "your_jwt_secret_key"
# ALGORITHM = "HS256"
#
# class AuthLogic:
#     def __init__(self, auth_repo: AuthRepository):
#         self.auth_repo = auth_repo
#
#     def create_access_token(data: dict, expires_delta: timedelta | None = None):
#         to_encode = data.copy()
#         if expires_delta:
#             expire = datetime.now(timezone.utc) + expires_delta
#         else:
#             expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#         return encoded_jwt
#
#     async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise credentials_exception
#             token_data = TokenData(username=username)
#         except JWTError:
#             raise credentials_exception
#         user = get_user(fake_users_db, username=token_data.username)
#         if user is None:
#             raise credentials_exception
#         return user
#
#     async def get_current_active_user(
#             current_user: Annotated[User, Depends(get_current_user)]
#     ):
#         if current_user.disabled:
#             raise HTTPException(status_code=400, detail="Inactive user")
#         return current_user