from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
import abc

from app.common.errors import ORMObjectExistsError, ORMIdIsRequiredError, ORMNoFieldsToUpdateError
from pydantic import BaseModel
from app.db.tables import DBBase


class BaseRepository(abc.ABC):
    ORM = DBBase
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session: AsyncSession = session

    @abc.abstractmethod
    def _get_orm(self) -> DBBase:
        '''Factory for `ORM` row representation.'''

    async def create(self) -> None:
        '''Insert new `Repository` to database.'''
        orm = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(orm)
        self.id = orm.id

    @classmethod
    @abc.abstractmethod
    def get_repository(cls, session: AsyncSession, orm: BaseModel) -> BaseRepository:
        '''Factory for `Repository` row representation.'''

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> BaseRepository:
        '''Select `Repository` by `id`.'''
        se = session
        async with session() as session:
            orm = await session.get(cls.ORM, id)

            if not orm:
                raise ORMObjectExistsError(cls.__name__, id)

        return cls.get_repository(se, orm)
    
    async def _update(self, fields: dict):
        '''Update `Repository` field. `Id` is required.'''
        if not self.id:
            raise ORMIdIsRequiredError()
        
        async with self.session() as session:
            async with session.begin():
                stmt = sa.update(self.ORM) \
                    .where(self.ORM.id == self.id) \
                    .values(fields)
                
                await session.execute(stmt)

    async def _modify(self, d: dict):
        '''Filters fields with `None` value. Then updates remaining ones.'''
        for key in d:
            if d[key] is None:
                del d[key]
        
        if not d:
            raise ORMNoFieldsToUpdateError()
        
        await self._update(d)

    @abc.abstractmethod
    async def modify(self, **args):
        '''Updates specified fields (passed as named arguments) in database.'''

    @property
    def session(self) -> AsyncSession:
        return self._session

    @session.setter
    def session(self, session: AsyncSession):
        self._session = session
