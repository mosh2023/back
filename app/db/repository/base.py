from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
import abc

from app.common.errors import ORMObjectNoFoundError, ORMIdIsRequiredError, \
    ORMNoFieldsToUpdateError, ORMUniqueFieldError, ORMRelationError
from pydantic import BaseModel
from app.db.tables import DBBase
from app.db.setup import async_session


class BaseRepository(abc.ABC):
    ORM = DBBase

    def __init__(self, session: AsyncSession = async_session) -> None:
        self._session = session
        super().__init__()

    @abc.abstractmethod
    def _get_orm(self) -> DBBase:
        '''Factory for `ORM` row representation.'''

    @abc.abstractmethod
    def get_model(self) -> BaseModel:
        '''Factory for `pydantic` row representation.'''

    async def create(self) -> None:
        '''Insert new `Repository` to database.'''
        orm = self._get_orm()
        try:
            async with self.session() as session:
                async with session.begin():
                    session.add(orm)
            self.id = orm.id
        except:
            raise ORMUniqueFieldError(orm)

    async def delete(self) -> None:
        '''Deletes `ORM` representation of this `Repository`.'''
        try:
            async with self.session() as session:
                async with session.begin():
                    stmt = sa.delete(self.ORM).where(self.ORM.id == self.id)
                    await session.execute(stmt)
            self.id = None
        except:
            raise ORMRelationError(self)

    @classmethod
    @abc.abstractmethod
    def get_repository(cls, orm: BaseModel, session: AsyncSession = async_session) -> BaseRepository:
        '''Factory for `Repository` row representation.'''

    @classmethod
    async def get(cls, id: int, session: AsyncSession = async_session) -> BaseRepository:
        '''Select `Repository` by `id`.'''
        se = session
        async with session() as session:
            orm = await session.get(cls.ORM, id)

            if not orm:
                raise ORMObjectNoFoundError(cls.__name__, id)

        return cls.get_repository(orm, se)

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
        for key in list(d.keys()):
            if d[key] is None:
                del d[key]
            elif d[key] == '':
                d[key] = None

        if not d:
            raise ORMNoFieldsToUpdateError(self.__class__.__name__, self.id)

        await self._update(d)

    @property
    def session(self) -> AsyncSession:
        return self._session

    @session.setter
    def session(self, session: AsyncSession):
        self._session = session
