from fastapi import APIRouter, HTTPException

from app.models.api import Id, GameInfo, GameEdit, PlayerMoves
from app.db.repository import Game, Player
from app.common.errors.db import ORMUniqueFieldError


router = APIRouter(
    prefix="/v1"
)


@router.post('/game', tags=['admin'])
async def create_game(game: GameInfo) -> Id:
    game: Game = Game.get_repository(game)
    # Resolve key, return `key` with Id.
    game.key = 'ABClass'
    try:
        await game.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=game.id)


@router.put('/game', tags=['admin'])
async def edit_game(game_edit: GameEdit):
    game: Game = await Game.get(game_edit.id)
    await game.modify(game_edit.name, game_edit.description, 
                game_edit.board_size)


@router.put('/player/add_moves', tags=['admin'])
async def add_moves(moves: PlayerMoves):
    player: Player = await Player.get(moves.id)
    await player.add_moves(moves.moves)
