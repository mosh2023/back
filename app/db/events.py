from app.db.setup import engine
from app.db.tables.base import get_metadata


async def init_db():
    metadata = get_metadata()

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def drop_db():
    metadata = get_metadata()

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
