from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from typing import Iterable
from datetime import datetime

from . import BaseRepository
from .player import Player
from .field import Field
from .boat import Boat
from .prize import Prize
from app.models.api import GameModel, GameAPIModel
from app.db.tables import GameORM, FieldORM, BoatORM, PrizeORM


class Game(BaseRepository):
    ORM = GameORM
    def __init__(self, session: AsyncSession, id: int | None, 
            name: str, description: str | None, board_size: int, key: str, 
            player1_id: int | None, player2_id: int | None, admin_id: int, 
            dt_start: datetime | None):
        super().__init__(session)

        self.id: int | None = id
        self.name: str = name
        self.description: str | None = description
        self.board_size: int = board_size 
        self.key: str = key 
        self.player1_id: int | None = player1_id
        self.player2_id: int | None = player2_id
        self.admin_id: int = admin_id
        self.dt_start: datetime | None = dt_start

    def _get_orm(self) -> GameORM:
        return GameORM(id=self.id, name=self.name, description=self.description, 
            board_size=self.board_size, key=self.key, player1_id=self.player1_id, 
            player2_id=self.player2_id, admin_id=self.admin_id, dt_start=self.dt_start)
    
    def get_model(self) -> GameModel:
        return GameModel(id=self.id, name=self.name, description=self.description, 
            board_size=self.board_size, key=self.key, player1_id=self.player1_id, 
            player2_id=self.player2_id, admin_id=self.admin_id, dt_start=self.dt_start)

    async def get_api_model(self) -> GameAPIModel:
        if self.player1_id:
            player1 = (await Player.get(self.session, self.player1_id)).get_model()
        else: player1 = None
        if self.player2_id:
            player2 = (await Player.get(self.session, self.player2_id)).get_model()
        else: player2 = None

        return GameAPIModel(id=self.id, name=self.name, description=self.description, 
            board_size=self.board_size, key=self.key, player1=player1, 
            player2=player2, admin_id=self.admin_id, dt_start=self.dt_start)

    @classmethod
    def get_repository(cls, session: AsyncSession, orm: GameModel) -> Game:
        id = orm.id if hasattr(orm, 'id') else None
        description = orm.description if hasattr(orm, 'description') else None
        key = orm.key if hasattr(orm, 'key') else None
        # Resolve key field. With login module.
        player1_id = orm.player1_id if hasattr(orm, 'player1_id') else None
        player2_id = orm.player2_id if hasattr(orm, 'player2_id') else None
        dt_start = orm.dt_start if hasattr(orm, 'dt_start') else None
        return Game(session, id, orm.name, description, orm.board_size, 
            key, player1_id, player2_id, orm.admin_id, dt_start)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Game:
        return await super().get(session, id)
    
    @classmethod
    async def get_by_key(cls, session: AsyncSession, key: str) -> Game | None:
        async with session() as session:
            game = await session.scalar(
                sa.select(GameORM)
                .where(GameORM.key == key)
            )
        if not game: return None
        return Game.get_repository(session, game)
    
    async def create(self) -> None:
        self.dt_start = datetime.now()
        await super().create()
    
    # add checker for board_size field. Тз чекай. Вынеси логику в __метод
    async def modify(self, name: str = None, description: str = None, board_size: int = None):
        if name is not None: self.name = name
        if description is not None: self.description = description
        if board_size is not None: self.board_size = board_size
        await self._modify({'name': name, 'description': description, 
                            'board_size': board_size})

    async def get_fields(self) -> Iterable[Field]:
        async with self.session() as session:
            fields = await session.scalars(
                sa.select(FieldORM)
                .where(FieldORM.game_id == self.id)
            )
            return (Field.get_repository(self.session, orm) for orm in fields)

    async def get_boats(self) -> Iterable[Boat]:
        async with self.session() as session:
            boats = await session.scalars(
                sa.select(BoatORM)
                .where(BoatORM.field.game_id == self.id)
            )
            return (Boat.get_repository(self.session, orm) for orm in boats)
        
    async def get_prizes(self) -> Iterable[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .join(PrizeORM.boat)
                .where(BoatORM.field.game_id == self.id)
            )
            return (Prize.get_repository(self.session, orm) for orm in prizes)

    def __repr__(self) -> str:
        return f'Game(id={self.id}, name="{self.name}", description=..., board_size={self.board_size}, ' \
            f'key=***, player1_id={self.player1_id}, player2_id={self.player2_id}, ' \
            f'admin_id={self.admin_id}, dt_start={self.dt_start})'
