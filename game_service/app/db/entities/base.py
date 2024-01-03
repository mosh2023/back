from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from app.common.errors import ORMObjectExistsError, ORMIdIsRequiredError
import abc

from app.db.tables import DBBase


class BaseEntity(abc.ABC):
    ORM = DBBase
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session: AsyncSession = session

    @abc.abstractmethod
    def _get_orm(self) -> DBBase:
        '''Factory for `ORM` row representation.'''

    async def create(self) -> None:
        '''Insert new entity to database.'''
        orm = self._get_orm()
        async with self.session() as session:
            async with session.begin():
                session.add(orm)
        self.id = orm.id

    @classmethod
    @abc.abstractmethod
    def _get_entity(cls, session: AsyncSession, orm: DBBase) -> BaseEntity:
        '''Factory for `Entity` row representation.'''

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> BaseEntity:
        '''Select entity by `id`.'''
        se = session
        async with session() as session:
            orm = await session.scalar(
                sa.select(cls.ORM)
                .where(cls.ORM.id == id)
            )

            if not orm:
                raise ORMObjectExistsError(cls.__name__, id)

        return cls._get_entity(se, orm)
    
    async def _update(self, par: str, value):
        '''Update entity field. `Id` is required.'''
        if not self.id:
            raise ORMIdIsRequiredError()
        
        async with self.session() as session:
            async with session.begin():
                stmt = sa.update(self.ORM).where(
                    self.ORM.id == self.id).values(
                    {par: value}
                )
                await session.execute(stmt)

    @property
    def session(self) -> AsyncSession:
        return self._session

    @session.setter
    def session(self, session: AsyncSession):
        self._session = session
