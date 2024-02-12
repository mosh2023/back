from fastapi import APIRouter
from app.models.api import GameKey, Hit


router = APIRouter(
    prefix="/mock"
)


@router.put('/game', tags=['player'])
async def join_game(key: GameKey):
    ...


@router.put('/game/hit', tags=['player'])
async def hit(hit: Hit):
    ...
