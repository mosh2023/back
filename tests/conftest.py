from asyncio import AbstractEventLoop
from typing import AsyncGenerator
from typing import Callable
import asyncio
import platform

from asyncpg.exceptions import InvalidCatalogNameError
from fastapi import FastAPI
from httpx import AsyncClient
from medsi_fastapi.app import MedsiFastApi
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
import pytest

from app.core.settings import APPSettings
from app.core.settings import get_app_settings
from app.db.tables.base import get_metadata
from tests.fixtures import *
from tests.mock import *


@pytest.fixture(scope="session")
def app_config() -> APPSettings:
    return get_app_settings()


@pytest.fixture(scope="session")
def map_models():
    yield get_metadata()


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def prepare_database(app_config: APPSettings):
    url = "?".join(("_".join((app_config.DATABASE_URL, "test")), "async_fallback=true"))
    engine = create_engine(url)

    try:
        database_exists(engine.url)
    except InvalidCatalogNameError:
        create_database(engine.url)
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
async def engine(app_config: APPSettings, prepare_database) -> AsyncEngine:
    engine = create_async_engine(
        "_".join((app_config.DATABASE_URL, "test")),
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_recycle=600,
        pool_use_lifo=True,
        pool_size=20,
        max_overflow=10,
    )

    yield engine


@pytest.fixture
async def connection(
    engine: AsyncEngine, map_models: MetaData
) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as connection:
        await connection.run_sync(map_models.drop_all)
        await connection.run_sync(map_models.create_all)
        yield connection


@pytest.fixture
async def db_session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    async_session: Callable = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession
    )
    async with async_scoped_session(async_session, asyncio.current_task)() as session:
        yield session
        await session.rollback()


@pytest.fixture
def get_session(db_session: AsyncSession):
    async def _override_get_session():
        yield db_session

    return _override_get_session


@pytest.fixture
def app(get_session: Callable) -> FastAPI:
    from app.api.dependencies.database import _get_session
    from app.main import app as fastapi_app

    MedsiFastApi.post_init(fastapi_app)
    fastapi_app.dependency_overrides[_get_session] = get_session

    return fastapi_app


@pytest.fixture
async def async_client(app: FastAPI, app_config: APPSettings) -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url=f"http://test{app_config.API_ROUTE}"
    ) as async_client:
        yield async_client
