from fastapi import APIRouter
from models.api import PlayerModel, PlayerInfo, PlayerEdit


router = APIRouter()


@router.get('/mock/profile/{player_id}')
async def get_profile() -> PlayerModel:
    return {'id': 2, 'auth_id': 3, 'name': 'V1adls1aV', 'icon_link': 'https://avatars.mds.yandex.net/i?id=33f11bfd4abc537a9ea0842a94d2987515232ff9-10843465-images-thumbs&n=13'}


@router.post('/mock/profile')
async def create_profile(player: PlayerInfo):
    ...


@router.put('/mock/profile')
async def edit_profile(player: PlayerEdit):
    ...

