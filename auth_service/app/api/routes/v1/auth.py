from fastapi import APIRouter


router = APIRouter()


@router.get('/auth')
async def auth():
    ...


@router.post('/auth')
async def register():
    ...


@router.put('/auth')
async def change_password():
    ...
