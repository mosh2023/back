from app.db.repository import User
from app.db.setup import async_session
import asyncio


async def main():
    u = await User.get(async_session, 2)
    print(u.icon_link)
    await u.modify(icon_link='https://i.pinimg.com/originals/72/52/ef/7252efee82102c8ac83c5659d945d63b.png')
    print(u.icon_link)
    uu = await User.get(async_session, 2)
    print(uu.icon_link)


asyncio.run(main())
