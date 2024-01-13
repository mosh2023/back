from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core import config

engine = create_async_engine(config.POSTGRES_URL, echo=config.DEBUG, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=True
)
