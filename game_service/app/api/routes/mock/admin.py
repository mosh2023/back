from fastapi import APIRouter


router = APIRouter()


@router.post('/mock/game')
async def create_game():
    ...


@router.post('/mock/game/boats')
async def create_boat():
    ...


@router.put('/mock/game/boats')
async def place_boat():
    ...


@router.put('/mock/game/hit')
async def add_shots():
    ...

