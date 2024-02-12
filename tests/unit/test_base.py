import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures import db_test_session
from app.services.common import generate_str
from app.db.repository import AuthRepository
from app.models.api import Roles


# Create an preparation function to set up database with 
# required rows. Raw sql?
@pytest.mark.asyncio
async def test_create(db_test_session: AsyncSession):
    auth: AuthRepository = AuthRepository(None, 
        generate_str(), generate_str(32), Roles.user, db_test_session)
    await auth.create()

    assert auth.id

    new_auth = await AuthRepository.get(auth.id, db_test_session)

    assert auth.get_model() == new_auth.get_model()


# async def test_update():
#     ...


# async def test_delete():
#     ...


# async def test_error():
#     ...
