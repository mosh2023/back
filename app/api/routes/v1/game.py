from fastapi import APIRouter
from app.models.api import GameAPIModel, FieldModel, BoatModel, PrizeModel
from typing import Optional
import asyncio

from app.db.repository import Game, User, Admin


router = APIRouter(
    prefix="/v1", tags=['game']
)


@router.get('/games/{user_id}')
async def get_games(user_id: int) -> list[GameAPIModel]:
    user: User = await User.get(user_id)
    return await asyncio.gather(
        *[game.get_api_model() for game in await user.get_games()])


@router.get('/admin_games/{admin_id}')
async def get_admin_games(admin_id: int) -> list[GameAPIModel]:
    admin: Admin = await Admin.get(admin_id)
    return await asyncio.gather(
        *[game.get_api_model() for game in await admin.get_games()])


@router.get('/game/{game_id}', tags=['game'])
async def get_game(game_id: int) -> Optional[GameAPIModel]:
    game: Game = await Game.get(game_id)
    return await game.get_api_model()


@router.get('/game/fields/{game_id}')
async def get_fields(game_id: int) -> list[FieldModel]:
    game: Game = await Game.get(game_id)
    return [field.get_model() for field in await game.get_fields()]


@router.get('/game/boats/{game_id}')
async def get_boats(game_id: int) -> list[BoatModel]:
    game: Game = await Game.get(game_id)
    return [boat.get_model() for boat in await game.get_boats()]


@router.get('/game/prizes/{game_id}')
async def get_prizes(game_id: int) -> list[PrizeModel]:
    game: Game = await Game.get(game_id)
    return [prize.get_model() for prize in await game.get_prizes()]