# import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from ...dependencies.postgresql import get_repository
#
# from app.db.repository.auth import AuthRepository
# from app.models.api.auth import AuthCreateRequest, AuthRequest, AuthResponse

router = APIRouter(
    prefix="/v1"
)

#
# @router.post("/register", tags=['auth'], response_model=AuthResponse)
# def register_user(user: AuthCreateRequest, db: Session = Depends(get_repository)):
#     auth_repo = AuthRepository(db)
#     auth_logic = AuthLogic(auth_repo)
#     existing_user = auth_repo.get_user_by_login(user.login)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Login already use")
#
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     new_user = auth_repo.create_user(login=user.login, password=hashed_password, role=user.role)
#     return new_user
#
#
# @router.post("/login", tags=['auth'])
# def login(user: AuthRequest, db: Session = Depends(get_repository)):
#     auth_repo = AuthRepository(db)
#     auth_logic = AuthLogic(auth_repo)
#     db_user = auth_logic.authenticate_user(user.login, user.password)
#
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Incorrect login or password")
#
#     access_token = auth_logic.create_access_token(user_id=db_user.id)
#     return {"access_token": access_token, "token_type": "bearer"}
