from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import FieldORM
from app.common.errors import ORMObjectExistsError


class Field(BaseEntity):
    ORM = FieldORM
    def __init__(self, session: AsyncSession, id: int | None,
            game_id: int, x: int, y: int, injured: bool, 
            player_id: int, boat_id: int):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.game_id: int = game_id
        self.x: int = x
        self.y: int = y
        self.injured: bool = injured
        self.player_id: int = player_id
        self.boat_id: int = boat_id

    def _get_orm(self) -> FieldORM:
        return FieldORM(id=self.id, game_id=self.game_id, x=self.x, y=self.y, 
            injured=self.injured, player_id=self.player_id, boat_id=self.boat_id)
    
    async def create(self) -> None:
        field = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(field)
        self.id = field.id

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: FieldORM) -> Field:
        return Field(session, orm.id, orm.game_id, orm.x, orm.y, 
            orm.injured, orm.player_id, orm.boat_id)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Field:
        se = session
        async with session() as session:
            field = await session.scalar(
                sa.select(FieldORM)
                .where(FieldORM.id == id)
            )

            if not field:
                raise ORMObjectExistsError(cls.__name__, id)

        return Field._get_entity(se, field)
    
    # def get_prize(self) -> Prize | None:
    #     ...

    def __repr__(self) -> str:
        return f'Field(id={self.id}, game_id={self.game_id}, x={self.x}, y={self.y},' \
            f'injured={self.injured}, player_id={self.player_id}, boat_id={self.boat_id})'

