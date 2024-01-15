from fastapi import APIRouter

from app.db.setup import async_session
from app.models.api import Id, GameInfo, GameEdit, PlayerMoves
from app.db.repository import Game, Player


router = APIRouter(
    prefix="/v1"
)


@router.post('/game', tags=['admin'])
async def create_game(game: GameInfo) -> Id:
    game: Game = Game.get_repository(async_session, game)
    await game.create()
    return Id(id=game.id)


@router.put('/game', tags=['admin'])
async def edit_game(game_edit: GameEdit):
    game: Game = await Game.get(async_session, game_edit.id)
    await game.modify(game_edit.name, game_edit.description, 
                game_edit.board_size)


@router.put('/game/hit', tags=['admin'])
async def add_shots(moves: PlayerMoves):
    player: Player = await Player.get(moves.id)
    await player.add_moves(moves.moves)
