from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

from app.core import config
from app.db.repository import AuthRepository
from app.models.api import Id, Token, AuthInfo, AuthResponse

router = APIRouter(
    prefix="/v1", tags=['auth']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(data: AuthInfo) -> Id:
    data.password = pwd_context.hash(data.password)
    auth: AuthRepository = AuthRepository.get_repository(data)
    await auth.create()
    return Id(id=auth.id)


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    auth: AuthRepository = await AuthRepository.get_by_login(form_data.username)
    if not auth or not verify_password(form_data.password, auth.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_data = AuthResponse(
        id=auth.id,
        login=auth.login,
        role=auth.role
    )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": auth_data.model_dump()}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
