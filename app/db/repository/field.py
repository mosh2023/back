from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.api import FieldModel
from app.db.tables import FieldORM
from app.db.setup import async_session


class Field(BaseRepository):
    ORM = FieldORM

    def __init__(self, id: int | None, game_id: int, x: int, y: int, injured: bool,
                 player_id: int | None = None, boat_id: int | None = None, session: AsyncSession = async_session):
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

    def get_model(self) -> FieldModel:
        return FieldModel(id=self.id, game_id=self.game_id, x=self.x, y=self.y,
                          injured=self.injured, player_id=self.player_id, boat_id=self.boat_id)

    @classmethod
    def get_repository(cls, orm: FieldModel, session: AsyncSession = async_session) -> Field:
        id = orm.id if hasattr(orm, 'id') else None
        player_id = orm.player_id if hasattr(orm, 'player_id') else None
        boat_id = orm.boat_id if hasattr(orm, 'boat_id') else None
        return Field(id, orm.game_id, orm.x, orm.y, orm.injured,
                     player_id, boat_id, session=session)

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> Field:
        return await super().get(id, session=session)

    @classmethod
    async def get_by_xy(cls, game_id: int, x: int, y: int,
                        session: AsyncSession = async_session) -> Field:
        async with session() as session:
            field = await session.scalar(
                sa.select(FieldORM)
                .where(sa.and_(
                    FieldORM.game_id == game_id,
                    FieldORM.x == x,
                    FieldORM.y == y
                ))
            )
        if not field: return None
        return Field.get_repository(field, session)

    async def set_boat(self, boat_id: int):
        self.boat_id = boat_id
        await self._update({'boat_id': boat_id})

    async def remove_boat(self):
        self.boat_id = None
        await self._update({'boat_id': None})

    def __repr__(self) -> str:
        return f'Field(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y},' \
               f'injured={self.injured}, player_id={self.player_id}, boat_id={self.boat_id})'
