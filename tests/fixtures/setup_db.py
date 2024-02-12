from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from functools import lru_cache

from .settings import config


@fixture
@lru_cache
def db_test_session() -> AsyncSession:
    engine = create_async_engine(config.POSTGRES_URL, 
        echo=config.DEBUG, future=True)
    async_session =  async_sessionmaker(
        engine, expire_on_commit=False, autoflush=True)
    return async_session
