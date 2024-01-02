from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import abc

from app.db.tables import DBBase


class BaseEntity(abc.ABC):
    ORM = DBBase
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    @abc.abstractmethod
    def _get_orm(self) -> DBBase:
        '''Factory for `ORM` row representation.'''

    @abc.abstractmethod
    async def create(self) -> None:
        '''Insert new entity to database.'''

    @classmethod
    @abc.abstractmethod
    def _get_entity(cls, session: AsyncSession, orm: DBBase) -> BaseEntity:
        '''Factory for `Entity` row representation.'''

    @classmethod
    @abc.abstractmethod
    async def get(cls, session: AsyncSession, id: int) -> BaseEntity:
        '''Select entity by `id`.'''

    @property
    def session(self) -> AsyncSession:
        return self._session

    @session.setter
    def session(self, session: AsyncSession):
        self._session = session
