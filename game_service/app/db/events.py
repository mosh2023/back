from app.db.setup import engine
from app.db.tables.base import get_metadata


async def init_db(from_meta=False):
    metadata = get_metadata()

    if from_meta:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
