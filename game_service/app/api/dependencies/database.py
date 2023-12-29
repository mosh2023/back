from typing import Any
from typing import AsyncGenerator
from typing import Callable
from typing import Coroutine
from typing import Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.entities import BaseEntity
from app.db.setup import async_session


async def _get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession
    async with async_session.begin() as session:
        yield session


def get_repository(
    repo_type: Type[BaseEntity],
) -> Callable[[AsyncSession], Coroutine[Any, Any, BaseEntity]]:
    async def _get_repo(
        session: AsyncSession = Depends(_get_session),
    ) -> BaseEntity:
        return repo_type(session)

    return _get_repo
