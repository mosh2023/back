from fastapi import APIRouter
from app.models.api import Id, GameInfo, GameEdit, GameMoves


router = APIRouter()


@router.post('/mock/game', tags=['admin'])
async def create_game(game: GameInfo) -> Id:
    return {'id': 1}


@router.put('/mock/game', tags=['admin'])
async def edit_game(game: GameEdit):
    ...


@router.put('/mock/game/hit', tags=['admin'])
async def add_shots(moves: GameMoves):
    ...

