from fastapi import APIRouter


router = APIRouter()


@router.put('/game')
async def join_game():
    ...


@router.put('/game/hit')
async def hit():
    ...
