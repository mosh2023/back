from fastapi import APIRouter
from app.models.api import Id, UserModel, UserInfo, UserEdit
from typing import Optional

router = APIRouter()


@router.get('/mock/user/{user_id}', tags=['user'])
async def get_profile(user_id: int) -> Optional[UserModel]:
    if user_id != 2: return None
    return {'id': 2, 
            'auth_id': 3, 
            'name': 'V1adls1aV', 
            'icon_link': 'https://avatars.mds.yandex.net/i?id=33f11bfd4abc537a9ea0842a94d2987515232ff9-10843465-images-thumbs&n=13'
            }
    # In `icon_link` field we will place link to Minio storage.


@router.post('/mock/user', tags=['user'])
async def create_user(player: UserInfo) -> Id:
    return {'id': 2}


@router.put('/mock/user', tags=['user'])
async def edit_user(player: UserEdit):
    ...

