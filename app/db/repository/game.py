from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from typing import Iterable
from datetime import datetime
import asyncio

from . import BaseRepository
from .player import Player
from .field import Field
from .boat import Boat
from .prize import Prize
from app.models.api import GameModel, GameAPIModel
from app.db.tables import GameORM, FieldORM, BoatORM, PrizeORM
from app.db.setup import async_session


class Game(BaseRepository):
    ORM = GameORM

    def __init__(self, id: int | None, name: str, description: str | None,
                 board_size: int, key: str, player1_id: int | None, player2_id: int | None,
                 admin_id: int, dt_start: datetime | None, session: AsyncSession = async_session):
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

    async def get_game_players(self) -> list[Player | None]:
        pls = [None, None]
        if self.player1_id and self.player2_id:
            pls = await asyncio.gather(
                Player.get(self.player1_id, self.session),
                Player.get(self.player2_id, self.session))
        elif self.player1_id:
            pls = [await Player.get(self.player1_id, self.session), None]
        elif self.player2_id:
            pls = [None, await Player.get(self.player2_id, self.session)]
        return pls

    async def get_api_model(self) -> GameAPIModel:
        player1, player2 = await self.get_game_players()
        if player1: player1 = player1.get_model()
        if player2: player2 = player2.get_model()
        return GameAPIModel(id=self.id, name=self.name, description=self.description,
                            board_size=self.board_size, key=self.key, player1=player1,
                            player2=player2, admin_id=self.admin_id, dt_start=self.dt_start)

    @classmethod
    def get_repository(cls, orm: GameModel, session: AsyncSession = async_session) -> Game:
        id = orm.id if hasattr(orm, 'id') else None
        description = orm.description if hasattr(orm, 'description') else None
        key = orm.key if hasattr(orm, 'key') else None
        # Resolve key field. With login module.
        player1_id = orm.player1_id if hasattr(orm, 'player1_id') else None
        player2_id = orm.player2_id if hasattr(orm, 'player2_id') else None
        dt_start = orm.dt_start if hasattr(orm, 'dt_start') else None
        return Game(id, orm.name, description, orm.board_size, key,
                    player1_id, player2_id, orm.admin_id, dt_start, session=session)

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> Game:
        return await super().get(id, session=session)

    @classmethod
    async def get_by_key(cls, key: str, session: AsyncSession = async_session) -> Game | None:
        async with session() as session:
            game = await session.scalar(
                sa.select(GameORM)
                .where(GameORM.key == key)
            )
        if not game: return None
        return Game.get_repository(game, session)

    async def create(self) -> None:
        self.dt_start = datetime.now()
        await super().create()

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
            return (Field.get_repository(orm, self.session) for orm in fields)
        
    async def get_injured_fields(self) -> Iterable[Field]:
        async with self.session() as session:
            fields = await session.scalars(
                sa.select(FieldORM)
                .where(sa.and_(
                    FieldORM.game_id == self.id,
                    FieldORM.injured == True
                ))
            )
            return (Field.get_repository(orm, self.session) for orm in fields)

    async def get_boats(self) -> Iterable[Boat]:
        async with self.session() as session:
            boats = await session.scalars(
                sa.select(BoatORM)
                .join(BoatORM.field)
                .where(FieldORM.game_id == self.id)
            )
            return (Boat.get_repository(orm, self.session) for orm in boats)
        
    async def get_won_boats(self) -> Iterable[Boat]:
        async with self.session() as session:
            boats = await session.scalars(
                sa.select(BoatORM)
                .join(BoatORM.field)
                .where(sa.and_(
                    FieldORM.game_id == self.id,
                    FieldORM.injured == True
                ))
            )
            return (Boat.get_repository(orm, self.session) for orm in boats)

    async def get_prizes(self) -> Iterable[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .join(PrizeORM.boat)
                .join(BoatORM.field)
                .where(FieldORM.game_id == self.id)
            )
            return (Prize.get_repository(orm, self.session) for orm in prizes)
        
    async def get_won_prizes(self) -> Iterable[Prize]:
        async with self.session() as session:
            prizes = await session.scalars(
                sa.select(PrizeORM)
                .join(PrizeORM.boat)
                .join(BoatORM.field)
                .where(sa.and_(
                    FieldORM.game_id == self.id, 
                    PrizeORM.user_id.is_not(None)
                ))
            )
            return (Prize.get_repository(orm, self.session) for orm in prizes)
        
    async def get_fullfields(self):
        async with self.session() as session:
            stmt = (sa.select(FieldORM, BoatORM, PrizeORM)
                .join(BoatORM, onclause=sa.and_(FieldORM.boat_id.is_not(None),
                                                FieldORM.boat_id == BoatORM.id), isouter=True)
                .join(PrizeORM, onclause=sa.and_(FieldORM.boat_id.is_not(None),
                                                BoatORM.prize_id == PrizeORM.id), isouter=True)
                .where(
                    FieldORM.game_id == self.id
                ))
            data = await session.execute(stmt)

            return ((Field.get_repository(field, self.session),
                     Boat.get_repository(boat, self.session) if boat else None,
                     Prize.get_repository(prize, self.session) if prize else None
                     ) for (field, boat, prize) in data)
        
    async def get_inj_fullfields(self):
        async with self.session() as session:
            stmt = (sa.select(FieldORM, BoatORM, PrizeORM)
                .join(BoatORM, onclause=sa.and_(FieldORM.boat_id.is_not(None),
                                                FieldORM.boat_id == BoatORM.id), isouter=True)
                .join(PrizeORM, onclause=sa.and_(FieldORM.boat_id.is_not(None),
                                                BoatORM.prize_id == PrizeORM.id), isouter=True)
                .where(sa.and_(
                    FieldORM.game_id == self.id,
                    FieldORM.injured == True
                )))
            data = await session.execute(stmt)

            return ((Field.get_repository(field, self.session),
                     Boat.get_repository(boat, self.session) if boat else None,
                     Prize.get_repository(prize, self.session) if prize else None
                     ) for (field, boat, prize) in data)

    def __repr__(self) -> str:
        return f'Game(id={self.id}, name="{self.name}", description=..., board_size={self.board_size}, ' \
               f'key=***, player1_id={self.player1_id}, player2_id={self.player2_id}, ' \
               f'admin_id={self.admin_id}, dt_start={self.dt_start})'
