from fastapi import APIRouter
from models.api import Id, GameInfo, GameEdit, GameMoves


router = APIRouter()


@router.post('/mock/game')
async def create_game(game: GameInfo) -> Id:
    return {'id': 1}


@router.put('/mock/game')
async def edit_game(game: GameEdit):
    ...


@router.put('/mock/game/hit')
async def add_shots(moves: GameMoves):
    ...

