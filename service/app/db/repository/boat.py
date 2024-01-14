from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.db import BoatDBModel
from app.db.tables import BoatORM


class Boat(BaseRepository):
    ORM = BoatORM
    def __init__(self, session: AsyncSession, id: int | None, prize_id: int):
        super().__init__(session)

        self.id: int | None = id
        self.prize_id: int = prize_id

    def _get_orm(self) -> BoatORM:
        return BoatORM(id=self.id, prize_id=self.prize_id)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: BoatDBModel) -> Boat:
        return Boat(session, orm.id, orm.prize_id)
    
    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Boat:
        return await super().get(session, id)

    def __repr__(self) -> str:
        return f'Field(id={self.id}, prize_id={self.prize_id})'

