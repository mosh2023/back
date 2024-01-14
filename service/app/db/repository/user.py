from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from .game import Game
from .prize import Prize
from app.models.db import UserDBModel
from app.db.tables import UserORM, PrizeORM, GameORM


class User(BaseRepository):
    ORM = UserORM
    def __init__(self, session: AsyncSession, id: int | None, 
            auth_id: int, name: str, icon_link: str = None):
        super().__init__(session)

        self.id: int | None = id
        self.auth_id: int = auth_id
        self.name: str = name
        self.icon_link: str = icon_link

    def _get_orm(self) -> UserORM:
        return UserORM(id=self.id, auth_id=self.auth_id, 
            name=self.name, icon_link=self.icon_link)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: UserDBModel) -> User:
        return User(session, orm.id, orm.auth_id, orm.name, orm.icon_link)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> User:
        return await super().get(session, id)

    async def modify(self, name: str = None, icon_link: str = None):
        if name is not None: self.name = name
        if icon_link is not None: self.icon_link = icon_link
        await self._modify({'name': name, 'icon_link': icon_link})

    async def get_games(self) -> list[Game]:
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .where((GameORM.player1.user_id == self.id) | 
                       (GameORM.player2.user_id == self.id))
            )
            return [Game.get_repository(self.session, orm) for orm in games]

    async def get_prizes(self) -> list[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.user_id == self.id)
            )
            return [Prize.get_repository(self.session, orm) for orm in prizes]
        
    async def join_game(self, key: str) -> Game:
        ...

    # Maybe move this to Player class
    async def leave_game(self, game_id: int):
        ...

    def __repr__(self) -> str:
        return f'User(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'
