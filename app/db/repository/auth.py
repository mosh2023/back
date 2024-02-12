from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.api import AuthModel
from app.db.tables import AuthORM
from app.db.setup import async_session


class AuthRepository(BaseRepository):
    ORM = AuthORM

    def __init__(self, id: int | None, login: str, password: str, role: str, session: AsyncSession = async_session):
        super().__init__(session)

        self.id: int | None = id
        self.login: str = login
        self.password: str = password
        self.role: str = role

    def _get_orm(self) -> AuthORM:
        return AuthORM(id=self.id, login=self.login, password=self.password, role=self.role)

    def get_model(self) -> AuthModel:
        return AuthModel(id=self.id, login=self.login, password=self.password, role=self.role)

    @classmethod
    def get_repository(cls, orm: AuthModel, session: AsyncSession = async_session) -> AuthRepository:
        id = orm.id if hasattr(orm, 'id') else None
        return AuthRepository(id, orm.login, orm.password, orm.role, session=session)

    @classmethod
    async def get_by_login(cls, login: str, session: AsyncSession = async_session) -> AuthRepository | None:
        async with session() as session:
            auth = await session.scalar(
                sa.select(AuthORM)
                .where(AuthORM.login == login)
            )
        if not auth: return None
        return AuthRepository.get_repository(auth, session)
