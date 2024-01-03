from app.db.entities import Player
from app.db.setup import async_session
import asyncio


async def main():
    id = 16
    player = Player(async_session, id, 13, 'Vlad')
    # await player.create()

    pl = await Player.get(async_session, id)
    print(pl)

    await pl.set_name('V1adls1aV')

    pl = await Player.get(async_session, id)
    print(pl)


if __name__ == '__main__':
    asyncio.run(main())
