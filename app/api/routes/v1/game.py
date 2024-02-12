from fastapi import APIRouter, Depends
from app.models.api import GameAPIModel, FieldModel, BoatModel, PrizeModel, AuthResponse, FullFieldModel
from typing import Optional
import asyncio

from app.db.repository import Game, User, Admin
from app.api.dependencies import require_user, require_admin


router = APIRouter(
    prefix="/v1", tags=['game']
)


@router.get('/games/{user_id}')
async def get_games(auth: AuthResponse = Depends(require_user)) -> list[GameAPIModel]:
    user: User = await User.get(auth.user_id)
    return await asyncio.gather(
        *[game.get_api_model() for game in await user.get_games()])


@router.get('/games/admin/{admin_id}')
async def get_admin_games(auth: AuthResponse = Depends(require_admin)) -> list[GameAPIModel]:
    admin: Admin = await Admin.get(auth.user_id)
    return await asyncio.gather(
        *[game.get_api_model() for game in await admin.get_games()])


@router.get('/game/{game_id}')
async def get_game(game_id: int) -> Optional[GameAPIModel]:
    game: Game = await Game.get(game_id)
    return await game.get_api_model()


@router.get('/game/fullfields/{game_id}')
async def get_user_fullfields(game_id: int, auth: AuthResponse = Depends(require_user)) -> list[FullFieldModel]:
    game: Game = await Game.get(game_id)
    data = await game.get_inj_fullfields()

    return [FullFieldModel(field=field.get_model(), \
        boat=(boat.get_model() if boat else None), \
        prize=(prize.get_model() if prize else None)) for field, boat, prize in data]


@router.get('/game/fullfields/admin/{game_id}')
async def get_admin_fullfields(game_id: int, auth: AuthResponse = Depends(require_admin)) -> list[FullFieldModel]:
    game: Game = await Game.get(game_id)
    data = await game.get_fullfields()

    return [FullFieldModel(field=field.get_model(), \
        boat=(boat.get_model() if boat else None), \
        prize=(prize.get_model() if prize else None)) for field, boat, prize in data]

