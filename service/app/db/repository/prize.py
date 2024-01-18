from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseRepository
from app.models.api import PrizeModel
from app.db.tables import PrizeORM
from datetime import datetime


class Prize(BaseRepository):
    ORM = PrizeORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, icon_link: str | None,
            user_id: int | None, admin_id: int, dt_won: datetime | None):
        super().__init__(session)

        self.id: int | None = id
        self.name: str = name
        self.description: str | None = description
        self.icon_link: str | None = icon_link
        self.user_id: int | None = user_id
        self.admin_id: int = admin_id
        self.dt_won: datetime | None = dt_won

    def _get_orm(self) -> PrizeORM:
        return PrizeORM(id=self.id, name=self.name, description=self.description,
            icon_link=self.icon_link, user_id=self.user_id, admin_id=self.admin_id,
            dt_won=self.dt_won)
    
    def get_model(self) -> PrizeModel:
        return PrizeModel(id=self.id, name=self.name, description=self.description,
            icon_link=self.icon_link, user_id=self.user_id, admin_id=self.admin_id,
            dt_won=self.dt_won)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: PrizeModel) -> Prize:
        id = orm.id if hasattr(orm, 'id') else None
        description = orm.description if hasattr(orm, 'description') else None
        icon_link = orm.icon_link if hasattr(orm, 'icon_link') else None
        user_id = orm.user_id if hasattr(orm, 'user_id') else None
        dt_won = orm.dt_won if hasattr(orm, 'dt_won') else None
        return Prize(session, id, orm.name, description, icon_link, 
            user_id, orm.admin_id, dt_won)

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

