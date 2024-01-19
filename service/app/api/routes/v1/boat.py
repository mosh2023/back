from fastapi import APIRouter

from app.models.api import Id, BoatInfo, BoatPlace
from app.db.repository import Boat, Field


router = APIRouter(
    prefix="/v1"
)


@router.post('/game/boats', tags=['boat'])
async def create_boat(boat: BoatInfo) -> Id:
    boat: Boat = Boat.get_repository(boat)
    await boat.create()
    return Id(id=boat.id)


@router.put('/game/boats', tags=['boat'])
async def place_boat(boat_place: BoatPlace):
    field: Field = Field(None, boat_place.game_id, 
        boat_place.x, boat_place.y, None, boat_place.id)
    await field.create()


@router.delete('/game/boats', tags=['boat'])
async def delete_boat(boat_id: Id):
    ...
