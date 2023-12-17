from typing import Type
from typing import TypeVar
import abc

from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(abc.ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @staticmethod
    def _map_db_object(row, to_schema: Type[T]) -> T:
        row = dict(row)

        return to_schema(**row)  # type: ignore
