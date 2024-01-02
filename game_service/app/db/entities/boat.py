from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import BoatORM


class Boat(BaseEntity):
    ORM = BoatORM
    def __init__(self, session: AsyncSession, id: int | None, prize_id: int):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.prize_id: int = prize_id

    def _get_orm(self) -> BoatORM:
        return BoatORM(id=self.id, prize_id=self.prize_id)

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: BoatORM) -> Boat:
        return Boat(session, orm.id, )
    
    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Boat:
        return await super().get(session, id)

    def __repr__(self) -> str:
        return f'Field(id={self.id}, prize_id={self.prize_id})'

