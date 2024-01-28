from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Response

from app.common.errors import ORMObjectNoFoundError, ORMUniqueFieldError
from app.db.repository import User
from app.models.api import Id, UserModel, UserInfo, UserEdit, AuthResponse
from app.api.dependencies import require_user
from app.services.user import save_icon
from app.api.dependencies import client


router = APIRouter(
    prefix="/v1", tags=['user']
)


@router.get('/user/{user_id}')
async def get_profile(user_id: int, auth: AuthResponse = Depends(require_user)) -> UserModel:
    try:
        user: User = await User.get(user_id)
        return user.get_model()
    except ORMObjectNoFoundError:
        raise HTTPException(404, f'User with id={user_id} does not exist.')


@router.post('/user')
async def create_user(user: UserInfo, auth: AuthResponse = Depends(require_user)) -> Id:
    user: User = User.get_repository(user)
    try:
        await user.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=user.id)


@router.put('/user')
async def edit_user(fields: UserEdit, auth: AuthResponse = Depends(require_user)):
    user: User = await User.get(fields.id)
    await user.modify(fields.name, fields.icon_link)
    print(user.icon_link)


# @router.post("/user/upload")
# async def upload_icon(file: UploadFile = File(...), auth: AuthResponse = Depends(require_user)):
#     return await save_icon(1, file.file, file.filename)
#
#
# @router.get("/download/{bucket}/{image}")
# async def download_image(bucket: str, image: str):
#     obj = client.get_object(Bucket=bucket, Key=image)
#     body = obj['Body'].read()
#     return Response(content=body, media_type="image/jpeg")
