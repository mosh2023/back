from fastapi import APIRouter
from app.models.api import Id, BoatInfo, BoatPlace


router = APIRouter()


@router.post('/mock/game/boats', tags=['boat'])
async def create_boat(boat: BoatInfo) -> Id:
    return {'id': 3}


# Edit boat? Not big deal I think.
@router.put('/mock/game/boats', tags=['boat'])
async def place_boat(boat: BoatPlace):
    ...


@router.delete('/mock/game/boats', tags=['boat'])
async def delete_boat(boat_id: Id):
    ...