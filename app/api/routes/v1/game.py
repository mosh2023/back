from fastapi import APIRouter, Depends
from app.models.api import GameAPIModel, FieldModel, BoatModel, PrizeModel, AuthResponse
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


@router.get('/game/fields/{game_id}')
async def get_injured_fields(game_id: int, auth: AuthResponse = Depends(require_user)) -> list[FieldModel]:
    '''Get injured Field models.'''
    game: Game = await Game.get(game_id)
    return [field.get_model() for field in await game.get_injured_fields()]


@router.get('/game/fields/admin/{game_id}')
async def get_admin_fields(game_id: int, auth: AuthResponse = Depends(require_admin)) -> list[FieldModel]:
    '''Full Field models.'''
    game: Game = await Game.get(game_id)
    return [field.get_model() for field in await game.get_fields()]


@router.get('/game/boats/{game_id}')
async def get_won_boats(game_id: int, auth: AuthResponse = Depends(require_user)) -> list[BoatModel]:
    '''Get Boats from hitted Fields.'''
    game: Game = await Game.get(game_id)
    return [boat.get_model() for boat in await game.get_won_boats()]


@router.get('/game/boats/admin/{game_id}')
async def get_admin_boats(game_id: int, auth: AuthResponse = Depends(require_admin)) -> list[BoatModel]:
    '''Full list of the Boats'''
    game: Game = await Game.get(game_id)
    return [boat.get_model() for boat in await game.get_boats()]


@router.get('/game/prizes/{game_id}')
async def get_won_prizes(game_id: int, auth: AuthResponse = Depends(require_user)) -> list[PrizeModel]:
    '''Only Prizes that have already been won.'''
    game: Game = await Game.get(game_id)
    return [prize.get_model() for prize in await game.get_won_prizes()]


@router.get('/game/prizes/admin/{game_id}')
async def get_all_prizes(game_id: int, auth: AuthResponse = Depends(require_admin)) -> list[PrizeModel]:
    '''Full list of the Prizes (won and placed)'''
    game: Game = await Game.get(game_id)
    return [prize.get_model() for prize in await game.get_prizes()]
