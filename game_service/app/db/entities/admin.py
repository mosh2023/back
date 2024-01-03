from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from .player import Player
from .game import Game
from .prize import Prize
from app.db.tables import PlayerORM, PrizeORM, GameORM


class Admin(Player):
    async def get_admin_games(self) -> list[Game]:
        se = self.session
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .where(GameORM.admin_id == self.id)
            )
            return [Game._get_entity(se, orm) for orm in games]
        
    async def get_admin_prizes(self) -> list[Prize]:
        se = self.session
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.admin_id == self.id)
            )
            return [Prize._get_entity(se, orm) for orm in prizes]
