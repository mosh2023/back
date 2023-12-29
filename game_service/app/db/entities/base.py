from sqlalchemy.ext.asyncio import AsyncSession
import abc

from app.db.tables import DBBase


class BaseEntity(abc.ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    @classmethod
    @abc.abstractmethod
    async def get(cls, session: AsyncSession, id: int):
        '''Select entity by `id`.'''

    @abc.abstractmethod
    async def create(self):
        '''Insert new entity to database.'''

    @abc.abstractmethod
    def _get_orm(self) -> DBBase:
        '''Factory for `ORM` row representation.'''

    @property
    def session(self) -> AsyncSession:
        return self._session
    
    @session.setter
    def session(self, session: AsyncSession):
        self._session = session
