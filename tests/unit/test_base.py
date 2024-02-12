import pytest
import unittest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures import db_test_session
from app.services.common import generate_str
from app.db.repository import BaseRepository, AuthRepository, User, Player, Game, Field, Boat, Prize
from app.models.api import Roles
from app.common.errors import ORMObjectNoFoundError


async def base_cycle(repo: BaseRepository):
    repo_cls = repo.__class__
    session = repo.session
    
    # Creating
    await repo.create()
    assert repo.id
    id = repo.id
    print(id)

    new_repo = await repo_cls.get(id, session)
    assert repo == new_repo

    # Updating
    attr = ...  # Dict with name of the modified repository fields
    if attr:
        ...

    # Deleting
    await repo.delete()
    print(repo)
    
    with unittest.TestCase().assertRaises(ORMObjectNoFoundError):
        new_repo = await repo_cls.get(id, session)



@pytest.mark.asyncio
async def test_base_auth(db_test_session: AsyncSession):
    # Run cycle with all the repositories.

    # auth: AuthRepository = AuthRepository(None, 
    #     generate_str(), generate_str(32), Roles.user, db_test_session)
    auth = User(None, 8, generate_str(), session=db_test_session)
    await base_cycle(auth)
    


# async def test_update():
#     ...


# async def test_delete():
#     ...


# async def test_error():
#     ...
