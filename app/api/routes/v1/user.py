from fastapi import APIRouter, HTTPException, File, UploadFile, Depends

from app.api.dependencies import verify_token
from app.common.errors import ORMObjectNoFoundError, ORMUniqueFieldError
from app.db.repository import User
from app.models.api import Id, UserModel, UserInfo, UserEdit, AuthResponse
from app.services.user import save_profile_picture, get_user_profile

router = APIRouter(
    prefix="/v1", tags=['user']
)


@router.get('/user/{user_id}')
async def get_profile(user_id: int, auth: AuthResponse = Depends(verify_token)) -> UserModel:
    try:
        return await get_user_profile(user_id)
    except ORMObjectNoFoundError:
        raise HTTPException(404, f'User with id={user_id} does not exist.')


@router.post('/user')
async def create_user(user: UserInfo, auth: AuthResponse = Depends(verify_token)) -> Id:
    try:
        await user.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=user.id)


@router.put('/user')
async def edit_user(fields: UserEdit, auth: AuthResponse = Depends(verify_token)):
    user: User = await User.get(fields.id)
    await user.modify(fields.name, fields.icon_link)


@router.post("/user/upload")
async def upload_user_icon(file: UploadFile = File(...), auth: AuthResponse = Depends(verify_token)):
    return await save_profile_picture(auth.user_id, file.file, file.filename)
