from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...dependencies.postgresql import get_repository
from app.models.api.auth import AuthCreateRequest, AuthResponse

router = APIRouter(
    prefix="/mock"
)


@router.post("/register", tags=['auth'], response_model=AuthResponse)
def register_user(user: AuthCreateRequest, db: Session = Depends(get_repository)):
    return ...


@router.post("/login", tags=['auth'])
def login(user: AuthCreateRequest, db: Session = Depends(get_repository)):
    return ...
