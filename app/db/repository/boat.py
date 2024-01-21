from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseRepository
from app.models.api import BoatModel
from app.db.tables import BoatORM
from app.db.setup import async_session


class Boat(BaseRepository):
    ORM = BoatORM

    def __init__(self, id: int | None, prize_id: int, session: AsyncSession = async_session):
        super().__init__(session)

        self.id: int | None = id
        self.prize_id: int = prize_id

    def _get_orm(self) -> BoatORM:
        return BoatORM(id=self.id, prize_id=self.prize_id)

    def get_model(self) -> BoatModel:
        return BoatModel(id=self.id, prize_id=self.prize_id)

    @classmethod
    def get_repository(cls, orm: BoatModel, session: AsyncSession = async_session) -> Boat:
        id = orm.id if hasattr(orm, 'id') else None
        return Boat(id, orm.prize_id, session=session)

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> Boat:
        return await super().get(id, session=session)

    def __repr__(self) -> str:
        return f'Field(id={self.id}, prize_id={self.prize_id})'
