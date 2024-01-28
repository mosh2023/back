from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import require_user
from app.db.repository import User, Player, Game, Field
from app.models.api import GameKey, Hit, PlayerModel, FullFieldModel
from app.models.api import Id, AuthResponse
from app.services.hit import get_player_ready_to_move, create_full_field_model

router = APIRouter(
    prefix="/v1", tags=['player']
)


@router.put('/player/join')
async def join_game(key: GameKey, auth: AuthResponse = Depends(require_user)) -> PlayerModel:
    game: Game = await Game.get_by_key(key.key)
    if not game:
        raise HTTPException(404, f'Game with key="{key.key}" does not found.')
    user: User = await User.get(key.user_id)
    player: Player = await user.join_game(game)

    if not player:
        raise HTTPException(400,
                            'You can not join this game. There are 2 players in the game or you have already joined it.')
    return player.get_model()


@router.put('/player/leave')
async def leave_game(player_id: Id, auth: AuthResponse = Depends(require_user)):
    player = await Player.get(player_id.id)
    await player.leave_game()


@router.put('/game/hit')
async def hit(hit: Hit, auth: AuthResponse = Depends(require_user)) -> FullFieldModel:
    field = await Field.get_by_xy(hit.game_id, hit.x, hit.y)

    if field is None:
        field = Field(id=None, game_id=hit.game_id,
                      x=hit.x, y=hit.y, injured=False)
        await field.create()
    elif field.injured:
        raise HTTPException(400, 'You can not hit the same field multiple times.')

    game = await Game.get(hit.game_id)
    player = await get_player_ready_to_move(game, hit.player_id)

    await player.hit(field)
    return await create_full_field_model(field, player.user_id)
