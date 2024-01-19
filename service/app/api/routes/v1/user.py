from fastapi import APIRouter, HTTPException

from app.models.api import Id, UserModel, UserInfo, UserEdit
from app.common.errors import ORMObjectExistsError
from app.db.repository import User


router = APIRouter(
    prefix="/v1"
)


@router.get('/user/{user_id}', tags=['user'])
async def get_profile(user_id: int) -> UserModel:
    try:
        user: User = await User.get(user_id)
        return user.get_model()
    except ORMObjectExistsError:
        raise HTTPException(404, f'User with id={user_id} does not exist.')


# Добавить проверку на наличие в метод `create`.
@router.post('/user', tags=['user'])
async def create_user(user: UserInfo) -> Id:
    user: User = User.get_repository(user)
    await user.create()
    return Id(id=user.id)


# Нужно ли возвращать юзера?
# Тут реальные проблемы с наличием поля `id` без него валидация не пропускает...
@router.put('/user', tags=['user'])
async def edit_user(fields: UserEdit):
    user: User = await User.get(fields.id)
    await user.modify(fields.name, fields.icon_link)
    print(user.icon_link)


