from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.db import PrizeDBModel
from app.db.tables import PrizeORM
from datetime import datetime


class Prize(BaseRepository):
    ORM = PrizeORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, icon_link: str | None,
            user_id: int | None, admin_id: int, dt_won: datetime | None):
        super().__init__(session)

        self.id: int | None = id
        name: str = name
        description: str | None = description
        icon_link: str | None = icon_link
        user_id: int | None = user_id
        admin_id: int = admin_id
        dt_won: datetime | None = dt_won

    def _get_orm(self) -> PrizeORM:
        return PrizeORM(id=self.id, name=self.name, description=self.description,
            icon_link=self.icon_link, user_id=self.user_id, admin_id=self.admin_id,
            dt_won=self.dt_won)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: PrizeDBModel) -> Prize:
        return Prize(session, orm.id, orm.name, orm.description, orm.icon_link, 
            orm.user_id, orm.admin_id, orm.dt_won)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Prize:
        return await super().get(session, id)
    
    async def modify(self, name: str = None, description: str = None, icon_link: str = None):
        if name is not None: self.name = name
        if description is not None: self.description = description
        if icon_link is not None: self.icon_link = icon_link
        await self._modify({'name': name, 'description': description, 
                            'icon_link': icon_link})
    
    async def set_winner(self, user_id: int):
        self.user_id = user_id
        self.dt_won = datetime.now()
        await self._update({'user_id': user_id,
                            'dt_won': self.dt_won})

    def __repr__(self) -> str:
        return f'Field(id={self.id}, name="{self.name}", description=..., ' \
            f'icon_link=..., user_id={self.user_id}, admin_id={self.admin_id}, ' \
            f'dt_won={self.dt_won})'

