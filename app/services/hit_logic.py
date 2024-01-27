from fastapi import HTTPException
import asyncio

from app.db.repository import Game, Player, Field, Boat, Prize
from app.models.api import FullFieldModel


async def get_player_ready_to_move(game: Game, player_id: int) -> Player:
    if game.player1_id and game.player2_id:
        player1, player2 = await asyncio.gather(
            Player.get(game.player1_id),
            Player.get(game.player2_id)
        )
        player = Player.whose_move_is(player1, player2)
        if not player or player.id != player_id:
            raise HTTPException(400, 'You can not hit the fields now. Maybe there is not your turn.')
    else:
        if game.player1_id == player_id:
            player = await Player.get(game.player1_id)
        elif game.player2_id == player_id:
            player = await Player.get(game.player2_id)
        else:
            raise HTTPException(400, 'You do not take part in this game.')
    
        if player.remaining_moves == 0:
            raise HTTPException(400, 'You do not have enough moves to hit the fields.')
        
    return player


async def create_full_field_model(field: Field, user_id: int):
    field_model, boat_model, prize_model = field.get_model(), None, None
    if field.boat_id:
        boat: Boat = await Boat.get(field.boat_id)
        prize: Prize = await Prize.get(boat.prize_id)
        await prize.set_winner(user_id)
        
        boat_model = boat.get_model()
        prize_model = prize.get_model()

    return FullFieldModel(
        field=field_model,
        boat=boat_model,
        prize=prize_model
    )