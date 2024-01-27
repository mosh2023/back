from fastapi import APIRouter, HTTPException, File, UploadFile

from app.models.api import Id, PrizeModel, PrizeInfo, PrizeEdit
from app.db.repository import User, Prize
from app.common.errors.db import ORMUniqueFieldError, ORMRelationError


router = APIRouter(
    prefix="/v1", tags=['prize']
)


@router.get('/prize/{user_id}')
async def get_prizes(user_id: int) -> list[PrizeModel]:
    user: User = await User.get(user_id)
    return [prize.get_model() for prize in await user.get_prizes()]


@router.post('/prize')
async def create_prize(prize: PrizeInfo) -> Id:
    prize: Prize = Prize.get_repository(prize)
    try:
        await prize.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=prize.id)


@router.put('/prize')
async def edit_prize(prize_edit: PrizeEdit):
    prize: Prize = await Prize.get(prize_edit.id)
    await prize.modify(prize_edit.name, prize_edit.description,
        prize_edit.icon_link)


@router.delete('/prize')
async def delete_prize(prize_id: Id):
    prize: Prize = await Prize.get(prize_id)
    try:
        await prize.delete()
    except ORMRelationError:
        raise HTTPException(400, f'You can not delete {prize} because of relation to another table.')


@router.post("/prize/upload")
async def upload_prize_picture(file: UploadFile = File(...)):
    return ...