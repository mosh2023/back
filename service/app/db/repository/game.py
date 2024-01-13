from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from datetime import datetime

from . import BaseRepository
from .field import Field
from .boat import Boat
from .prize import Prize
from app.db.tables import GameORM, FieldORM, BoatORM, PrizeORM


class Game(BaseRepository):
    ORM = GameORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, board_size: int, key: str, 
            player_id: int, player_moves: int, admin_id: int, 
            dt_start: datetime | None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        name: str = name
        description: str | None = description
        board_size: int = board_size 
        key: str = key 
        player_id: int | None = player_id
        player_moves: int = player_moves
        admin_id: int = admin_id
        dt_start: datetime | None = dt_start

    def _get_orm(self) -> GameORM:
        return GameORM(
            id=self.id, name=self.name, description=self.description, board_size=self.board_size, 
            key=self.key, player_id=self.player_id, player_moves=self.player_moves, 
            admin_id=self.admin_id, dt_start=self.dt_start
        )

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: GameORM) -> Game:
        return GameORM(session, orm.id, orm.name, orm.description, orm.board_size, 
            orm.key, orm.player_id, orm.player_moves, orm.admin_id, orm.dt_start)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Game:
        return await super().get(session, id)
    
    async def set_name(self, name: str):
        self.name = name
        await self._update('name', name)
    
    async def set_description(self, description: str):
        self.description = description
        await self._update('description', description)


    async def is_move_available(self) -> bool:
        ...

    async def move(self):
        ...

    async def add_moves(self, num):
        ...

    async def get_fields(self) -> list[Field]:
        se = self.session
        async with self.session() as session:
            fields = await session.scalars(
                sa.select(FieldORM)
                .where(FieldORM.game_id == self.id)
            )
            return [Field._get_entity(se, orm) for orm in fields]

    async def get_boats(self) -> list[Boat]:
        ...
        
    async def get_prizes(self) -> list[Prize]:
        ...

    def __repr__(self) -> str:
        return f'Game(id={self.id}, name="{self.name}", description=..., board_size={self.board_size}, ' \
            f'key=***, player_id={self.player_id}, player_moves={self.player_moves}, ' \
            f'admin_id={self.admin_id}, dt_start={self.dt_start})'
