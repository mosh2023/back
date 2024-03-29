from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import require_admin
from app.models.api import Id, BoatInfo, BoatPlace, AuthResponse
from app.db.repository import Boat, Field
from app.common.errors.db import ORMUniqueFieldError, ORMRelationError

router = APIRouter(
    prefix="/v1", tags=['boat']
)


@router.post('/game/boat')
async def create_boat(boat: BoatInfo, auth: AuthResponse = Depends(require_admin)) -> Id:
    boat: Boat = Boat.get_repository(boat)
    try:
        await boat.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=boat.id)


@router.put('/game/boat/place')
async def place_boat(boat_place: BoatPlace, auth: AuthResponse = Depends(require_admin)):
    field: Field = await Field.get_by_xy(boat_place.game_id, boat_place.x, boat_place.y)
    if field is not None:
        if not field.boat_id:
            await field.set_boat(boat_place.id)
        else:
            raise HTTPException(400, 'There is already a boat in this field.')
    else:
        field = Field(None, boat_place.game_id, boat_place.x,
                      boat_place.y, False, None, boat_place.boat_id)
        await field.create()


@router.put('/game/field/remove')
async def remove_boat(field_id: Id, auth: AuthResponse = Depends(require_admin)):
    field: Field = await Field.get(field_id.id)
    await field.remove_boat()


@router.delete('/game/boat/delete/{boat_id}')
async def delete_boat(boat_id: int, auth: AuthResponse = Depends(require_admin)):
    boat: Boat = await Boat.get(boat_id)
    try:
        await boat.delete()
    except ORMRelationError:
        raise HTTPException(400, f'You can not delete {boat} because of relation to another table.')
