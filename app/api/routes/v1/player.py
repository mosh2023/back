from fastapi import APIRouter, HTTPException


from app.models.api import Id, GameKey, Hit, PlayerModel, FieldModel
from app.db.repository import User, Player, Game, Field


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
        raise HTTPException(400, 'You can not join this game. There are 2 players in the game or you have already joined it.')
    return player.get_model()


@router.put('/player/leave')
async def leave_game(player_id: Id):
    player = await Player.get(player_id.id)
    await player.leave_game()


@router.put('/game/hit', tags=['player'])
async def hit(hit: Hit) -> FieldModel:
    field = await Field.get_by_xy(hit.game_id, hit.x, hit.y)

    if field is None:
        field = Field(id=None, game_id=hit.game_id, 
            x=hit.x, y=hit.y, injured=False)
        await field.create()
    elif field.injured:
        raise HTTPException(400, 'You can not hit the same field multiple times.')
    
    game = await Game.get(hit.game_id)

    if game.player1_id and game.player2_id:
        player1 = await Player.get(game.player1_id)
        player2 = await Player.get(game.player2_id)

        player = Player.whose_move_is(player1, player2)
        if not player or player.id != hit.player_id:
            raise HTTPException(400, 'You can not hit the fields now. Maybe there is not your turn.')
    elif game.player1_id == hit.player_id:
        player = await Player.get(game.player1_id)
    elif game.player2_id == hit.player_id:
        player = await Player.get(game.player2_id)
    else: 
        raise HTTPException(400, 'You do not have enough moves to hit the fields.')

    await player.hit(field)
    return field.get_model()
    # For checking boat/prize in this field.
    # Maybe return a whole field-boat-prize objects with prize?

