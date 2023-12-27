from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core import config


DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=config.DEBUG, future=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=True
)
