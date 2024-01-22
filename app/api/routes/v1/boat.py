from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import require_admin
from app.models.api import Id, BoatInfo, BoatPlace, AuthResponse
from app.db.repository import Boat, Field
from app.common.errors.db import ORMUniqueFieldError


router = APIRouter(
    prefix="/v1", tags=['boat']
)


@router.post('/game/boats')
async def create_boat(boat: BoatInfo, auth: AuthResponse = Depends(require_admin)) -> Id:
    boat: Boat = Boat.get_repository(boat)
    try:
        await boat.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=boat.id)


@router.put('/game/boats')
async def place_boat(boat_place: BoatPlace, auth: AuthResponse = Depends(require_admin)):
    field: Field = Field(None, boat_place.game_id, 
        boat_place.x, boat_place.y, None, boat_place.id)
    await field.create()


@router.delete('/game/boats')
async def delete_boat(boat_id: Id):
    ...
