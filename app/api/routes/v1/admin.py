from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import require_admin
from app.common.errors.db import ORMUniqueFieldError
from app.db.repository import Game, Player
from app.models.api import GameId, GameInfo, GameEdit, PlayerMoves, AuthResponse
from app.services.game_logic import generate_key


router = APIRouter(
    prefix="/v1", tags=['admin']
)


@router.post('/game')
async def create_game(game: GameInfo, auth: AuthResponse = Depends(require_admin)) -> GameId:
    game: Game = Game.get_repository(game)

    key = generate_key()
    game.key = key
    try:
        await game.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return GameId(id=game.id, key=key)


@router.put('/game')
async def edit_game(game_edit: GameEdit, auth: AuthResponse = Depends(require_admin)):
    game: Game = await Game.get(game_edit.id)
    await game.modify(game_edit.name, game_edit.description,
                      game_edit.board_size)


@router.put('/player/add_moves')
async def add_moves(moves: PlayerMoves, auth: AuthResponse = Depends(require_admin)):
    player: Player = await Player.get(moves.id)
    await player.add_moves(moves.moves)
