from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseEntity
from app.db.tables import PlayerORM
from app.common.errors import ORMObjectExistsError


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
    
    async def create(self) -> None:
        player = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(player)
        self.id = player.id

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: PlayerORM) -> Player:
        return Player(session, orm.id, orm.auth_id, orm.name, orm.icon_link)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Player:
        se = session
        async with session() as session:
            player = await session.scalar(
                sa.select(PlayerORM)
                .where(PlayerORM.id == id)
            )

            if not player:
                raise ORMObjectExistsError(cls.__name__, id)

        return Player._get_entity(se, player)

    # def get_games(self, admin: bool) -> list[Game]:
    #     '''Split this to multiple methods. Rely on `role` parameter.'''

    # def get_prizes(self) -> list[Prize]:
    #     ...

    def __repr__(self) -> str:
        return f'Player(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'

