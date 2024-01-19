from __future__ import annotations
from typing import Iterable
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .user import User
from .game import Game
from .prize import Prize
from app.db.tables import PrizeORM, GameORM
from app.models.api import UserModel
from app.db.setup import async_session


class Admin(User):
    @classmethod
    def get_repository(cls, orm: UserModel, session: AsyncSession = async_session) -> User:
        id = orm.id if hasattr(orm, 'id') else None
        icon_link = orm.icon_link if hasattr(orm, 'icon_link') else None
        return Admin(id, orm.auth_id, orm.name, icon_link, session=session)
    
    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> Admin:
        return await super().get(id, session=session)

    async def get_games(self) -> Iterable[Game]:
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .where(GameORM.admin_id == self.id)
            )
        return (Game.get_repository(orm, self.session) for orm in games)
        
    async def get_prizes(self) -> Iterable[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.admin_id == self.id)
            )
        return (Prize.get_repository(orm, self.session) for orm in prizes)

    def __repr__(self) -> str:
        return f'Admin(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'

