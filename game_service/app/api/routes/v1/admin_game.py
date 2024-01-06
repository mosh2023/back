from fastapi import APIRouter


router = APIRouter()


@router.post('/game')
async def create_game():
    ...


@router.post('/game/boats')
async def create_boat():
    ...


@router.put('/game/boats')
async def place_boat():
    ...


@router.put('/game/hit')
async def add_shots():
    ...

