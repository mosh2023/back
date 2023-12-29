from app.db.entities import Player
from app.db.setup import async_session
import asyncio


async def main():
    player = Player(async_session, None, 1, 'Vlad')
    await player.create()

    pl = await Player.get(async_session, player.id)
    print(pl)


if __name__ == '__main__':
    asyncio.run(main())
