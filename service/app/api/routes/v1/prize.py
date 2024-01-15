from fastapi import APIRouter
from app.models.api import Id, PrizeModel, PrizeInfo, PrizeEdit

from app.db.setup import async_session
from app.db.repository import User, Prize


router = APIRouter(
    prefix="/v1"
)


@router.get('/prizes/{user_id}', tags=['prize'])
async def get_prizes(user_id: int) -> list[PrizeModel]:
    user: User = await User.get(async_session, user_id)
    return [prize.get_model() for prize in await user.get_prizes()]


@router.post('/prizes', tags=['prize'])
async def create_prize(prize: PrizeInfo) -> Id:
    prize: Prize = Prize.get_repository(async_session, prize)
    await prize.create()
    return Id(id=prize.id)


@router.put('/prizes', tags=['prize'])
async def edit_prize(prize_edit: PrizeEdit):
    prize: Prize = await Prize.get(prize_edit.id)
    await prize.modify(prize_edit.name, prize_edit.description,
        prize_edit.icon_link)


@router.delete('/prizes')
async def delete_prize(prize_id: Id):
    ...

