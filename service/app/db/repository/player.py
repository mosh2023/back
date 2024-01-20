from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.api import PlayerModel
from app.db.tables import PlayerORM, GameORM
from app.db.setup import async_session


class Player(BaseRepository):
    ORM = PlayerORM
    def __init__(self, id: int | None, user_id: int, remaining_moves: int = 0, 
            used_moves: int = 0, session: AsyncSession = async_session):
        super().__init__(session)

        self.id: int | None = id
        self.user_id: int = user_id
        self.remaining_moves: int = remaining_moves
        self.used_moves: int = used_moves

    def _get_orm(self) -> PlayerORM:
        return PlayerORM(id=self.id, user_id=self.user_id, 
            remaining_moves=self.remaining_moves, used_moves=self.used_moves)
    
    def get_model(self) -> PlayerModel:
        return PlayerModel(id=self.id, user_id=self.user_id, 
            remaining_moves=self.remaining_moves, used_moves=self.used_moves)

    @classmethod
    def get_repository(cls, orm: PlayerModel, session: AsyncSession = async_session) -> Player:
        id = orm.id if hasattr(orm, 'id') else None
        return Player(id, orm.user_id, orm.remaining_moves, 
            orm.used_moves, session=session)

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> Player:
        return await super().get(id, session=session)
    
    @staticmethod
    async def whose_move_is(player1: PlayerModel, player2: PlayerModel) -> PlayerModel | None:
        if (player1.used_moves + player2.used_moves) % 2:
            if player2.remaining_moves: return player2
            elif player1.remaining_moves: return player1
        else:
            if player1.remaining_moves: return player1
            elif player2.remaining_moves: return player2
        return None
    
    async def add_moves(self, moves: int):
        self.remaining_moves += moves
        async with self.session() as session:
            async with session.begin():
                stmt = sa.update(PlayerORM) \
                    .where(PlayerORM.id == self.id) \
                    .values(remaining_moves=PlayerORM.remaining_moves + moves)
                
                await session.execute(stmt)

    async def leave_game(self):
        async with self.session() as session:
            async with session.begin():
                stmt = sa.update(GameORM) \
                    .where((GameORM.player1_id == self.id) | 
                           (GameORM.player2_id == self.id)) \
                    .values(
                        player1_id=sa.case(
                            (GameORM.player1_id == self.id, None),
                            else_=GameORM.player1_id
                        ),
                        player2_id=sa.case(
                            (GameORM.player2_id == self.id, None),
                            else_=GameORM.player2_id
                        )
                    )

                await session.execute(stmt)

    def __repr__(self) -> str:
        return f'Player(id={self.id}, user_id={self.user_id}, ' \
            f'remaining_moves={self.remaining_moves}, used_moves={self.used_moves})'
