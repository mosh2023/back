from fastapi import APIRouter
from app.models.api import GameModel, FieldModel, BoatModel, PrizeModel
from datetime import datetime
from typing import Optional


router = APIRouter()


@router.get('/mock/games/{player_id}', tags=['game'])
async def get_games(player_id: int) -> list[GameModel]:
    if player_id != 2: return []
    return [{'id': 1,
             'name': 'TheFirstGame',
             'description': 'smth about',
             'board_size': 7,
             'key': 'ARSA12',
             'player1': {
                 'id': 1,
                 'user_id': 1,
                 'remaining_moves': 2,
                 'used_moves': 1
             },
             'player2': {
                 'id': 2,
                 'user_id': 2,
                 'remaining_moves': 3,
                 'used_moves': 2
             },
             'game_id': 3,
             'dt_start': datetime.now()
            },
            {'id': 2,
             'name': 'TheSecondGame',
             'board_size': 5,
             'key': 'URSU23',
             'player1': {
                 'id': 2,
                 'user_id': 2,
                 'remaining_moves': 1,
                 'used_moves': 0
             },
             'game_id': 1
             }]


@router.get('/mock/game/{game_id}', tags=['game'])
async def get_game(game_id: int) -> Optional[GameModel]:
    if game_id != 1: return None
    return {'id': 1,
             'name': 'TheFirstGame',
             'description': 'smth about',
             'board_size': 7,
             'key': 'ARSA12',
             'player1': {
                 'id': 1,
                 'user_id': 1,
                 'remaining_moves': 2,
                 'used_moves': 1
             },
             'player2': {
                 'id': 2,
                 'user_id': 2,
                 'remaining_moves': 3,
                 'used_moves': 2
             },
             'game_id': 3,
             'dt_start': datetime.now()
            }


@router.get('/mock/game/fields/{game_id}')
async def get_fields(game_id: int) -> list[FieldModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'game_id': 1,
             'x': 0,
             'y': 3,
             'injured': True,
             'player_id': 2
            },
            {'id': 2,
             'game_id': 1,
             'x': 5,
             'y': 3,
             'injured': True,
             'player_id': 2,
             'boat_id': 1,
            },
            {'id': 1,
             'game_id': 1,
             'x': 4,
             'y': 6,
             'injured': False,
             'boat_id': 2
            }]


@router.get('/mock/game/boats/{game_id}')
async def get_boats(game_id: int) -> list[BoatModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'prize_id': 2
            },
            {'id': 2,
             'prize_id': 1
            }]


@router.get('/mock/game/prizes/{game_id}')
async def get_prizes(game_id: int) -> list[PrizeModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'name': 'Промокод 500 биомашинкоинов',
             'game_id': 2,
             'user_id': 4
            },
            {'id': 2,
             'name': 'Полтос от Владоса',
             'description': 'То, чего ты так долго ждал.',
             'icon_link': 'https://avatars.mds.yandex.net/i?id=afd3bff4da0e5925c9b786ebc086b8a895c23666-10590187-images-thumbs&n=13',
             # In `icon_link` field we will place link to Minio storage.
             'game_id': 2,
             'user_id': 4,
             'dt_won': datetime.now()
            }]