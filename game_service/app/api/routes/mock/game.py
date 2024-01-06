from fastapi import APIRouter
from models.api import GameModel
from datetime import datetime

router = APIRouter()


@router.get('/mock/games/{player_id}')
async def get_games() -> list[GameModel]:
    return [{'id': 1, 'name': 'TheFirstGame', 'description': 'smth about', 'board_size': 7, 'player_id': 3, 'player_moves': 4, 'admin_id': 2, 'dt_start': datetime.now()}, 
            {'id': 2, 'name': 'TheSecondGame', 'board_size': 5, 'player_id': 2, 'player_moves': 1, 'admin_id': 1}]


@router.get('/mock/game/{game_id}')
async def get_game():
    return {'id': 1, 'name': 'TheFirstGame', 'description': 'smth about', 'board_size': 7, 'player_id': 3, 'player_moves': 4, 'admin_id': 2, 'dt_start': datetime.now()}


@router.get('/mock/fields/{game_id}')
async def get_fields():
    ...


@router.get('/mock/boats/{game_id}')
async def get_boats():
    ...


@router.get('/mock/prizes/{game_id}')
async def get_prizes():
    ...

