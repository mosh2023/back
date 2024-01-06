from fastapi import APIRouter


router = APIRouter()


@router.get('/prizes/{player_id}')
async def get_prizes():
    ...


@router.post('/prizes')
async def create_prize():
    ...


@router.put('/prizes')
async def edit_prize():
    ...


@router.delete('/prizes')
async def delete_prize():
    ...

