from sqlalchemy.orm import Session
from .base import BaseRepository
from ..tables.auth import AuthORM


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_login(self, login: str):
        return self.db.query(AuthORM).filter(AuthORM.login == login).first()

    def create_user(self, login: str, password: str, role: str):

        new_auth = AuthORM(login=login, password=password, role=role)
        self.db.add(new_auth)
        self.db.commit()
        self.db.refresh(new_auth)
        return new_auth
