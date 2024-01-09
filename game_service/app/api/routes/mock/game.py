from fastapi import APIRouter
from models.api import GameModel, FieldModel, BoatModel, PrizeModel
from datetime import datetime

router = APIRouter()


@router.get('/mock/games/{player_id}')
async def get_games(player_id: int) -> list[GameModel]:
    if player_id != 2: return []
    return [{'id': 1,
             'name': 'TheFirstGame',
             'description': 'smth about',
             'board_size': 7,
             'key': 'ARSA12',
             'player_id': 2,
             'player_moves': 4,
             'admin_id': 3,
             'dt_start': datetime.now()
            },
            {'id': 2,
             'name': 'TheSecondGame',
             'board_size': 5,
             'key': 'URSU23',
             'player_id': 2,
             'player_moves': 1,
             'admin_id': 1
             }]


@router.get('/mock/game/{game_id}')
async def get_game(game_id: int) -> GameModel:
    if game_id != 1: return None
    return {'id': 1,
            'name': 'TheFirstGame',
            'description': 'smth about',
            'board_size': 7,
            'key': 'URSU23',
            'player_id': 2,
            'player_moves': 4,
            'admin_id': 3,
            'dt_start': datetime.now()
            }


@router.get('/mock/fields/{game_id}')
async def get_fields(game_id: int) -> list[FieldModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'game_id': 1,
             'x': 0,
             'y': 3,
             'injured': True
            },
            {'id': 2,
             'game_id': 1,
             'x': 5,
             'y': 3,
             'injured': True,
             'boat_id': 1,
            },
            {'id': 1,
             'game_id': 1,
             'x': 4,
             'y': 6,
             'injured': False,
             'boat_id': 2
            }]


@router.get('/mock/boats/{game_id}')
async def get_boats(game_id: int) -> list[BoatModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'prize_id': 2
            },
            {'id': 2,
             'prize_id': 1
            }]


@router.get('/mock/prizes/{game_id}')
async def get_prizes(game_id: int) -> list[PrizeModel]:
    if game_id != 1: return []
    return [{'id': 1,
             'name': 'Промокод 500 биомашинкоинов',
             'admin_id': 2,
             'player_id': 4
            },
            {'id': 2,
             'name': 'Полтос от Владоса',
             'description': 'То, чего ты так долго ждал.',
             'icon_link': 'https://avatars.mds.yandex.net/i?id=afd3bff4da0e5925c9b786ebc086b8a895c23666-10590187-images-thumbs&n=13',
             'admin_id': 2,
             'player_id': 4,
             'dt_won': datetime.now()
            }]
