from fastapi import APIRouter


router = APIRouter()


@router.get('/profile/{player_id}')
async def get_profile():
    ...


@router.post('/profile')
async def create_profile():
    ...


@router.put('/profile')
async def edit_profile():
    ...

