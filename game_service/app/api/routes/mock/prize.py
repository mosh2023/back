from fastapi import APIRouter
from app.models.api import Id, PrizeModel, PrizeInfo, PrizeEdit
from datetime import datetime


router = APIRouter()


@router.get('/mock/prizes/{player_id}')
async def get_prizes(player_id: int) -> list[PrizeModel]:
    if player_id != 2: return []
    return [{'id': 4,
             'name': 'The Best Prize',
             'admin_id': 1,
             'user_id': 2,
             'dt_won': datetime.now()}]


@router.post('/mock/prizes')
async def create_prize(prize: PrizeInfo) -> Id:
    return {'id': 5}


@router.put('/mock/prizes')
async def edit_prize(prize: PrizeEdit):
    ...


@router.delete('/mock/prizes')
async def delete_prize(prize_id: Id):
    ...

