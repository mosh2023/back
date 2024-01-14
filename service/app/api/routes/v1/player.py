from fastapi import APIRouter, HTTPException

from app.db.setup import async_session
from app.models.api import GameKey, Hit
from app.db.repository import User, Player, Game


router = APIRouter()


@router.put('/mock/game', tags=['player'])
async def join_game(key: GameKey) -> Player:
    game: Game = Game.get_by_key(key.key)
    if not game:
        raise HTTPException(404, f'Game with key="{key.key}" does not found.')
    user: User = User.get(async_session, key.user_id)
    player: Player = user.join_game(game)
    
    if not player:
        raise HTTPException(400, 'You can not join this game. It already has have 2 players.')
    return player.get_model()
    

@router.put('/mock/game/hit', tags=['player'])
async def hit(hit: Hit):
    ...
