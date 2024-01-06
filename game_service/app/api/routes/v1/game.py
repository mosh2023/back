from fastapi import APIRouter


router = APIRouter()


@router.get('/games')
async def get_games():
    ...


@router.get('/game')
async def get_game():
    ...


@router.get('fields/{game_id}')
async def get_fields():
    ...


@router.get('boats/{game_id}')
async def get_boats():
    ...


@router.get('prizes/{game_id}')
async def get_prizes():
    ...

