from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from .base import BaseRepository
from app.db.tables.auth import AuthORM
from app.models.db import Roles, AuthDBModel


class Auth(BaseRepository):
    ORM = AuthORM
    def __init__(self, session: AsyncSession, id: int | None,
            login: str, password: str, role: Roles):
        super().__init__(session)

        self.id: int = id
        self.login: str = login
        self.password: str = password
        self.role: Roles = role

    def _get_orm(self) -> AuthORM:
        return AuthORM(id=self.id, login=self.login,
            password=self.password, role=self.role)

    def get_model(self) -> AuthDBModel:
        return AuthDBModel(id=self.id, login=self.login,
            password=self.password, role=self.role)
    
    @classmethod
    def get_repository(cls, session: AsyncSession, orm: AuthDBModel) -> Auth:
        return Auth(session, orm.id, orm.login, orm.password, orm.role)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Auth:
        return await super().get(session, id)
    
    @classmethod
    async def get_by_login(self, login: str) -> Auth:
        async with self.session as session:
            auth = await session.scalar(
                sa.select(AuthORM)
                .where(AuthORM.login == login)
            )
        return Auth.get_repository(session, auth)

    async def change_password(self, password: str):
        self.password = password
        self._update({'password': self.password})

    def __repr__(self) -> str:
        return f'Auth(id={self.id}, login={self.login}, password=***, role={self.role})'
