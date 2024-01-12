from fastapi import APIRouter
from app.models.api import GameKey, Hit


router = APIRouter()


@router.put('/mock/game')
async def join_game(key: GameKey):
    ...


@router.put('/mock/game/hit')
async def hit(hit: Hit):
    ...
