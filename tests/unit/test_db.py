from app.db.tables import *
from tests.conftest import *
import sqlalchemy as sa
import pytest


@pytest.mark.asyncio
async def test_registration(db_session):
    # engine = sa.create_engine('')
    # Session = sa.orm.sessionmaker(engine)
    session = anext(db_session)
    
    print('#' * 20, session)

    player = PlayerORM(name='Vlad')
    session.add(player)
    session.commit()

    p = session.scalar(
        sa.select(PlayerORM))
    
    assert p.name == 'Vlad'


# async def test_personal_account():
#     ...


# async def test_game_creation():
#     ...


# async def test_game_start():
#     ...


# async def test_game_process():
#     ...


# async def test_game_end():
#     ...
