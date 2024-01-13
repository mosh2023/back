from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from .prize import Prize
from .boat import Boat
from app.db.tables import FieldORM, BoatORM, PrizeORM


class Field(BaseRepository):
    ORM = FieldORM
    def __init__(self, session: AsyncSession, id: int | None,
            game_id: int, x: int, y: int, injured: bool, boat_id: int | None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.game_id: int = game_id
        self.x: int = x
        self.y: int = y
        self.injured: bool = injured
        self.boat_id: int | None = boat_id

    def _get_orm(self) -> FieldORM:
        return FieldORM(id=self.id, game_id=self.game_id, x=self.x, y=self.y, 
            injured=self.injured, boat_id=self.boat_id)

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: FieldORM) -> Field:
        return Field(session, orm.id, orm.game_id, orm.x, orm.y, 
            orm.injured, orm.boat_id)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Field:
        return await super().get(session, id)
    
    def get_prize(self) -> Prize | None:
        ...

    # Автосоздание поля
    def hit(self):
        ...

    def __repr__(self) -> str:
        return f'Field(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y},' \
            f'injured={self.injured}, boat_id={self.boat_id})'

