from fastapi import APIRouter
from app.models.api import GameKey, Hit


router = APIRouter()


@router.put('/mock/game', tags=['player'])
async def join_game(key: GameKey):
    ...


@router.put('/mock/game/hit', tags=['player'])
async def hit(hit: Hit):
    ...
