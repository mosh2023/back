from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, status

from app.api.dependencies import verify_token
from app.common.errors import ORMObjectNoFoundError, ORMUniqueFieldError
from app.db.repository import User
from app.models.api import Id, UserModel, UserInfo, UserEdit, AuthResponse
from app.services.user import save_profile_picture, get_user_profile

router = APIRouter(
    prefix="/v1", tags=['user']
)


@router.get('/user/{user_id}')
async def get_profile(auth: AuthResponse = Depends(verify_token)) -> UserModel:
    try:
        return await get_user_profile(auth.user_id)
    except ORMObjectNoFoundError:
        raise HTTPException(404, f'User with id={auth.user_id} does not exist.')


@router.post('/user')
async def create_user(user: UserInfo, auth: AuthResponse = Depends(verify_token)) -> Id:
    try:
        await user.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=user.id)


@router.put('/user')
async def edit_user(fields: UserEdit, auth: AuthResponse = Depends(verify_token)):
    user: User = await User.get(auth.user_id)
    await user.modify(fields.name, fields.icon_link)


@router.post("/user/upload")
async def upload_user_icon(file: UploadFile = File(...), auth: AuthResponse = Depends(verify_token)):
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type {file.content_type}"
        )
    icon_link = await save_profile_picture(auth.user_id, file.file, file.filename)
    if icon_link is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload file.")
    return icon_link
