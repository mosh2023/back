from fastapi import APIRouter


router = APIRouter()


@router.get('/mock/prizes/{player_id}')
async def get_prizes():
    ...


@router.post('/mock/prizes')
async def create_prize():
    ...


@router.put('/mock/prizes')
async def edit_prize():
    ...


@router.delete('/mock/prizes')
async def delete_prize():
    ...

