from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from datetime import datetime

from . import BaseEntity
from app.db.tables import GameORM


class Game(BaseEntity):
    ORM = GameORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, board_size: int, key: str, 
            player1_id: int, player1_remaining_moves: int, player1_used_moves: int, 
            player2_id: int, player2_remaining_moves: int, player2_used_moves: int, 
            admin_id: int, datetime_start: datetime | None, datetime_end: datetime | None):
        super().__init__(session)
        self._session: AsyncSession = session

        self.id: int | None = id
        name: str = name
        description: str | None = description
        board_size: int = board_size 
        key: str = key 
        player1_id: int | None = player1_id
        player1_remaining_moves: int = player1_remaining_moves
        player1_used_moves: int = player1_used_moves
        player2_id: int | None = player2_id
        player2_remaining_moves: int = player2_remaining_moves
        player2_used_moves: int = player2_used_moves
        admin_id: int = admin_id
        datetime_start: datetime | None = datetime_start
        datetime_end: datetime | None = datetime_end

    def _get_orm(self) -> GameORM:
        return GameORM(
            id=self.id, name=self.name, description=self.description, board_size=self.board_size, key=self.key, 
            player1_id=self.player1_id, player1_remaining_moves=self.player1_remaining_moves, player1_used_moves=self.player1_used_moves,
            player2_id=self.player2_id, player2_remaining_moves=self.player2_remaining_moves, player2_used_moves=self.player2_used_moves,
            admin_id=self.admin_id, datetime_start=self.datetime_start, datetime_end=self.datetime_end
        )

    @classmethod
    def _get_entity(cls, session: AsyncSession, orm: GameORM) -> Game:
        return GameORM(session, orm.id, orm.name, orm.description, orm.board_size, orm.key, 
            orm.player1_id, orm.player1_remaining_moves, orm.player1_used_moves,
            orm.player2_id, orm.player2_remaining_moves, orm.player2_used_moves,
            orm.admin_id, orm.datetime_start, orm.datetime_end)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Game:
        return await super().get(session, id)

    # Не бизнес ли логика?
    def whose_move(self):
        ...

    def is_move_available(self, player_id, x, y) -> bool:
        ...

    def move(self, player_id, x, y):
        ...

    def add_moves(self, player_id, num) -> None:
        ...

    # def get_fields(self) -> list[Field]:
    #     ...

    # def get_prizes(self) -> list[Prize]:
    #     ...

    def __repr__(self) -> str:
        return f'Game(id={self.id}, name="{self.name}", description=..., board_size={self.board_size}, key=***, ' \
            f'player1_id={self.player1_id}, player1_remaining_moves={self.player1_remaining_moves}, player1_used_moves={self.player1_used_moves}, ' \
            f'player2_id={self.player2_id}, player2_remaining_moves={self.player2_remaining_moves}, player2_used_moves={self.player2_used_moves}, ' \
            f'admin_id={self.admin_id}, datetime_start={self.datetime_start}, datetime_end={self.datetime_end})'
