from fastapi import APIRouter, HTTPException

from app.models.api import Id, UserModel, UserInfo, UserEdit
from app.common.errors import ORMObjectNoFoundError, ORMUniqueFieldError
from app.db.repository import User

router = APIRouter(
    prefix="/v1", tags=['user']
)


@router.get('/user/{user_id}')
async def get_profile(user_id: int) -> UserModel:
    try:
        user: User = await User.get(user_id)
        return user.get_model()
    except ORMObjectNoFoundError:
        raise HTTPException(404, f'User with id={user_id} does not exist.')


@router.post('/user')
async def create_user(user: UserInfo) -> Id:
    user: User = User.get_repository(user)
    try:
        await user.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=user.id)


@router.put('/user')
async def edit_user(fields: UserEdit):
    user: User = await User.get(fields.id)
    await user.modify(fields.name, fields.icon_link)
    print(user.icon_link)
