from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import PrizeORM
from app.common.errors import ORMObjectExistsError
from datetime import datetime as dt


class Prize(BaseEntity):
    ORM = PrizeORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, icon_link: str | None,
            player_id: int | None, admin_id: int, datetime: dt | None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        name: str = name
        description: str | None = description
        icon_link: str | None = icon_link
        player_id: int | None = player_id
        admin_id: int = admin_id
        datetime: dt | None = datetime

    def _get_orm(self) -> PrizeORM:
        return PrizeORM(id=self.id, name=self.name, description=self.description,
            icon_link=self.icon_link, player_id=self.player_id, admin_id=self.admin_id,
            datetime=self.datetime)
    
    async def create(self) -> None:
        prize = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(prize)
        self.id = prize.id

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PrizeORM) -> Prize:
        return Prize(session, orm.id, orm.name, orm.description, orm.icon_link, 
            orm.player_id, orm.admin_id, orm.datetime)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Prize:
        se = session
        async with session() as session:
            prize = await session.scalar(
                sa.select(PrizeORM)
                .where(PrizeORM.id == id)
            )

            if not prize:
                raise ORMObjectExistsError(cls.__name__, id)

        return Prize._get_entity(se, prize)

    def __repr__(self) -> str:
        return f'Field(id={self.id}, name="{self.name}", description=..., ' \
            f'icon_link=..., player_id={self.player_id}, admin_id={self.admin_id}, ' \
            f'datetime={self.datetime})'

