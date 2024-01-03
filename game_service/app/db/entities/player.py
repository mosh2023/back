from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from .game import Game
from .prize import Prize
from app.db.tables import PlayerORM, PrizeORM, GameORM


class Player(BaseEntity):
    ORM = PlayerORM
    def __init__(self, session: AsyncSession, id: int | None, 
            auth_id: int, name: str, icon_link: str = None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.auth_id: int = auth_id
        self.name: str = name
        self.icon_link: str = icon_link

    def _get_orm(self) -> PlayerORM:
        return PlayerORM(id=self.id, auth_id=self.auth_id, 
            name=self.name, icon_link=self.icon_link)

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PlayerORM) -> Player:
        return Player(session, orm.id, orm.auth_id, orm.name, orm.icon_link)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Player:
        return await super().get(session, id)

    async def set_name(self, name: str):
        self.name = name
        await self._update('name', name)

    async def set_icon_link(self, icon_link: str):
        self.icon_link = icon_link
        await self._update('icon_link', icon_link)

    async def get_games(self) -> list[Game]:
        se = self.session
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .where(GameORM.player_id == self.id)
            )
            return [Game._get_entity(se, orm) for orm in games]

    async def get_prizes(self) -> list[Prize]:
        se = self.session
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.player_id == self.id)
            )
            return [Prize._get_entity(se, orm) for orm in prizes]

    def __repr__(self) -> str:
        return f'Player(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'

