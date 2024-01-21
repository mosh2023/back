from fastapi import APIRouter
from app.models.api import Id, GameInfo, GameEdit, PlayerMoves


router = APIRouter(
    prefix="/mock"
)


@router.post('/game', tags=['admin'])
async def create_game(game: GameInfo) -> Id:
    return {'id': 1}


@router.put('/game', tags=['admin'])
async def edit_game(game: GameEdit):
    ...


@router.put('/game/hit', tags=['admin'])
async def add_shots(moves: PlayerMoves):
    ...

