from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.db.tables import PrizeORM
from datetime import datetime


class Prize(BaseRepository):
    ORM = PrizeORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, icon_link: str | None,
            player_id: int | None, admin_id: int, dt_won: datetime | None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        name: str = name
        description: str | None = description
        icon_link: str | None = icon_link
        player_id: int | None = player_id
        admin_id: int = admin_id
        dt_won: datetime | None = dt_won

    def _get_orm(self) -> PrizeORM:
        return PrizeORM(id=self.id, name=self.name, description=self.description,
            icon_link=self.icon_link, player_id=self.player_id, admin_id=self.admin_id,
            dt_won=self.dt_won)

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PrizeORM) -> Prize:
        return Prize(session, orm.id, orm.name, orm.description, orm.icon_link, 
            orm.player_id, orm.admin_id, orm.dt_won)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Prize:
        return await super().get(session, id)
    
    async def set_name(self, name: str):
        self.name = name
        await self._update('name', name)
    
    async def set_description(self, description: str):
        self.description = description
        await self._update('description', description)
    
    async def set_winner(self):
        # Привязать автоматом дату выигрыша.
        ...

    def __repr__(self) -> str:
        return f'Field(id={self.id}, name="{self.name}", description=..., ' \
            f'icon_link=..., player_id={self.player_id}, admin_id={self.admin_id}, ' \
            f'dt_won={self.dt_won})'

