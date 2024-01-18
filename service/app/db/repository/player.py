from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from . import BaseRepository
from app.models.api import PlayerModel, GamePlayers
from app.db.tables import PlayerORM, GameORM


class Player(BaseRepository):
    ORM = PlayerORM
    def __init__(self, session: AsyncSession, id: int | None, 
            user_id: int, remaining_moves: int = 0, used_moves: int = 0):
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
    def get_repository(cls, session: AsyncSession, orm: PlayerModel) -> Player:
        id = orm.id if hasattr(orm, 'id') else None
        return Player(session, id, orm.user_id, 
            orm.remaining_moves, orm.used_moves)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Player:
        return await super().get(session, id)
    
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

    async def leave_game(self, game: GamePlayers):
        players = [game.player1_id, game.player2_id]
        if None not in players:
            return None
        player_num = players.index(None)
        pl = f'player{player_num + 1}_id'

        async with self.session() as session:
            async with session.begin():
                stmt = sa.update(GameORM) \
                    .where(getattr(GameORM, pl) == self.id) \
                    .values({pl: None})

                await session.execute(stmt)

    def __repr__(self) -> str:
        return f'Player(id={self.id}, user_id={self.user_id}, ' \
            f'remaining_moves={self.remaining_moves}, used_moves={self.used_moves})'
