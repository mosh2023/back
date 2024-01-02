from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import PrizeORM
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

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PrizeORM) -> Prize:
        return Prize(session, orm.id, orm.name, orm.description, orm.icon_link, 
            orm.player_id, orm.admin_id, orm.datetime)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Prize:
        return await super().get(session, id)
    
    def set_winner(self):
        # Привязать автоматом дату выигрыша.
        ...

    def __repr__(self) -> str:
        return f'Field(id={self.id}, name="{self.name}", description=..., ' \
            f'icon_link=..., player_id={self.player_id}, admin_id={self.admin_id}, ' \
            f'datetime={self.datetime})'

