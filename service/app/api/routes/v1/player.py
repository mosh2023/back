from fastapi import APIRouter, HTTPException


from app.models.api import GameKey, Hit, PlayerModel
from app.db.repository import User, Player, Game


router = APIRouter(
    prefix="/v1"
)


@router.put('/player/join')
async def join_game(key: GameKey) -> PlayerModel:
    game: Game = await Game.get_by_key(key.key)
    if not game:
        raise HTTPException(404, f'Game with key="{key.key}" does not found.')
    user: User = await User.get(key.user_id)
    player: Player = await user.join_game(game)
    
    if not player:
        raise HTTPException(400, 'You can not join this game. It already has have 2 players.')
    return player.get_model()


@router.put('/player/leave')
async def leave_game(p):
    ...
    

@router.put('/game/hit', tags=['player'])
async def hit(hit: Hit):
    ...
