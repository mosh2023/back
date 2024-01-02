from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import BoatORM
from app.common.errors import ORMObjectExistsError


class Boat(BaseEntity):
    ORM = BoatORM
    def __init__(self, session: AsyncSession, id: int | None, prize_id: int):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.prize_id: int = prize_id

    def _get_orm(self) -> BoatORM:
        return BoatORM(id=self.id, prize_id=self.prize_id)
    
    async def create(self) -> None:
        boat = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(boat)
        self.id = boat.id

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: BoatORM) -> Boat:
        return Boat(session, orm.id, )

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Boat:
        se = session
        async with session() as session:
            boat = await session.scalar(
                sa.select(BoatORM)
                .where(BoatORM.id == id)
            )

            if not boat:
                raise ORMObjectExistsError(cls.__name__, id)

        return Boat._get_entity(se, boat)

    def __repr__(self) -> str:
        return f'Field(id={self.id}, prize_id={self.prize_id})'

