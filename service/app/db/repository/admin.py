from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from .user import User
from .game import Game
from .prize import Prize
from app.db.tables import PrizeORM, GameORM


class Admin(User):
    async def join_game(self, key: str) -> Game:
        ...

    async def leave_game(self, game_id: int):
        ...

    async def get_games(self) -> list[Game]:
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .where(GameORM.admin_id == self.id)
            )
            return [Game.get_repository(self.session, orm) for orm in games]
        
    async def get_prizes(self) -> list[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.admin_id == self.id)
            )
            return [Prize.get_repository(self.session, orm) for orm in prizes]
