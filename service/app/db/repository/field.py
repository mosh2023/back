from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from .prize import Prize
from .boat import Boat
from app.models.db import FieldDBModel
from app.db.tables import FieldORM


class Field(BaseRepository):
    ORM = FieldORM
    def __init__(self, session: AsyncSession, id: int | None, game_id: int, 
            x: int, y: int, injured: bool, player_id: int | None, boat_id: int | None):
        super().__init__(session)

        self.id: int | None = id
        self.game_id: int = game_id
        self.x: int = x
        self.y: int = y
        self.injured: bool = injured
        self.player_id: int | None = player_id
        self.boat_id: int | None = boat_id

    def _get_orm(self) -> FieldORM:
        return FieldORM(id=self.id, game_id=self.game_id, x=self.x, y=self.y, 
            injured=self.injured, player_id=self.player_id, boat_id=self.boat_id)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: FieldDBModel) -> Field:
        return Field(session, orm.id, orm.game_id, orm.x, orm.y, 
            orm.injured, orm.player_id, orm.boat_id)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Field:
        return await super().get(session, id)

    # Тут надо продумать, может обернуть в classmethod. + автосоздание
    def hit(self, player_id: int):
        self.injured = True
        self.player_id = player_id
        self._update({'injured': True,
                      'player_id': player_id})

    def __repr__(self) -> str:
        return f'Field(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y},' \
            f'injured={self.injured}, player_id={self.player_id}, boat_id={self.boat_id})'

