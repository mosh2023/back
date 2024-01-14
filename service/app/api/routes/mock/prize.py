from fastapi import APIRouter
from app.models.api import Id, PrizeModel, PrizeInfo, PrizeEdit
from datetime import datetime


router = APIRouter(
    prefix="/mock"
)


@router.get('/prizes/{player_id}', tags=['prize'])
async def get_prizes(player_id: int) -> list[PrizeModel]:
    if player_id != 2: return []
    return [{'id': 4,
             'name': 'The Best Prize',
             'prize_id': 1,
             'user_id': 2,
             'dt_won': datetime.now()}]


@router.post('/prizes', tags=['prize'])
async def create_prize(prize: PrizeInfo) -> Id:
    return {'id': 5}


@router.put('/prizes', tags=['prize'])
async def edit_prize(prize: PrizeEdit):
    ...


@router.delete('/prizes')
async def delete_prize(prize_id: Id):
    ...

