from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import PlayerORM


class Player(BaseEntity):
    ORM = PlayerORM
    def __init__(self, session: AsyncSession, id: int | None, 
            auth_id: int, name: str, icon_link: str = None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        self.auth_id: int = auth_id
        self.name: str = name
        self.icon_link: str = icon_link

    def _get_orm(self) -> PlayerORM:
        return PlayerORM(id=self.id, auth_id=self.auth_id, 
            name=self.name, icon_link=self.icon_link)

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PlayerORM) -> Player:
        return Player(session, orm.id, orm.auth_id, orm.name, orm.icon_link)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Player:
        return await super().get(session, id)

    # def get_games(self, role: Enum) -> list[Game]:
    #     '''Split this to multiple methods. Rely on `role` parameter.'''

    # def get_prizes(self) -> list[Prize]:
    #     ...

    def __repr__(self) -> str:
        return f'Player(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'

