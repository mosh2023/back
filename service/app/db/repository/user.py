from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from typing import Iterable

from . import BaseRepository
from .player import Player
from .game import Game
from .prize import Prize
from app.models.api import UserModel, Id
from app.db.tables import UserORM, PlayerORM, PrizeORM, GameORM
from app.db.setup import async_session


class User(BaseRepository):
    ORM = UserORM
    def __init__(self, id: int | None, auth_id: int, name: str, 
            icon_link: str | None = None, session: AsyncSession = async_session):
        super().__init__(session)

        self.id: int | None = id
        self.auth_id: int = auth_id
        self.name: str = name
        self.icon_link: str | None = icon_link

    def _get_orm(self) -> UserORM:
        return UserORM(id=self.id, auth_id=self.auth_id, 
            name=self.name, icon_link=self.icon_link)
        
    def get_model(self) -> UserModel:
        return UserModel(id=self.id, auth_id=self.auth_id, 
            name=self.name, icon_link=self.icon_link)

    @classmethod
    def get_repository(cls, orm: UserModel, session: AsyncSession = async_session) -> User:
        id = orm.id if hasattr(orm, 'id') else None
        icon_link = orm.icon_link if hasattr(orm, 'icon_link') else None
        return User(id, orm.auth_id, orm.name, icon_link, session=session)

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> User:
        return await super().get(id, session=session)

    async def modify(self, name: str = None, icon_link: str = None):
        if name is not None: self.name = name
        if icon_link is not None: self.icon_link = icon_link
        await self._modify({'name': name, 'icon_link': icon_link})

    async def get_games(self) -> Iterable[Game]:
        async with self.session() as session:
            games = await session.scalars(
                sa.select(GameORM)
                .join(PlayerORM, sa.or_(GameORM.player1, GameORM.player2))
                .where(PlayerORM.user_id == self.id)
            )
        return (Game.get_repository(orm, self.session) for orm in games)

    async def get_prizes(self) -> Iterable[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .where(PrizeORM.user_id == self.id)
            )
        return (Prize.get_repository(orm, self.session) for orm in prizes)
    
    async def join_game(self, game: Id) -> Player | None:
        async with self.session() as session:    
            async with session.begin():
                user_ids = await session.scalars(sa.select(PlayerORM.user_id) \
                    .join(GameORM, sa.or_(PlayerORM.game1, PlayerORM.game2)) \
                    .where(GameORM.id == game.id))
            
                if self.id in user_ids:
                    await session.close()
                    return None
                
                player = PlayerORM(user_id=self.id, remaining_moves=0, used_moves=0)
                session.add(player)
                await session.flush()

                stmt = sa.update(GameORM) \
                    .where(GameORM.id == game.id) \
                    .values(
                        player1_id=sa.case((
                                GameORM.player1_id.is_(None), player.id),
                            else_=GameORM.player1_id
                        ),
                        player2_id=sa.case((
                            sa.and_(
                                GameORM.player1_id.is_not(None), 
                                GameORM.player2_id.is_(None)
                            ), player.id),
                            else_=GameORM.player2_id
                        )
                    )
                await session.execute(stmt)

        game: Game = await Game.get(game.id, session=self.session)

        if player.id == game.player1_id or player.id == game.player2_id:
            return Player.get_repository(player, self.session)
        return None

    def __repr__(self) -> str:
        return f'User(id={self.id}, auth_id={self.auth_id}, name="{self.name}", icon_link=...)'

