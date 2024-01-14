import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...dependencies.postgresql import get_repository
from app.logic.auth_logic import AuthLogic
from app.db.repository.auth import AuthRepository
from app.models.api.auth import AuthCreateRequest, AuthRequest, AuthResponse

router = APIRouter()


@router.post("/register", tags=['auth'], response_model=AuthResponse)
def register_user(user: AuthCreateRequest, db: Session = Depends(get_repository)):
    return ...


@router.post("/login", tags=['auth'])
def login(user: AuthCreateRequest, db: Session = Depends(get_repository)):
    return ...
