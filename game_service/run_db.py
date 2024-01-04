from app.db.entities import Player
from app.db.setup import async_session
import asyncio


async def main():
    id = 3
    # player = Player(async_session, id, 15, 'Vlad')
    # await player.create()

    pl = await Player.get(async_session, id)
    print(pl)

    await pl.set_name('Alexander')

    pl = await Player.get(async_session, id)
    print(pl)


if __name__ == '__main__':
    asyncio.run(main())
