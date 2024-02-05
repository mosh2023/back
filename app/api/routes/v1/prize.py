from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, status

from app.api.dependencies import require_admin
from app.common.errors.db import ORMUniqueFieldError, ORMRelationError
from app.db.repository import User, Prize
from app.models.api import Id, AuthResponse
from app.models.api import PrizeModel, PrizeInfo, PrizeEdit
from app.services.prize import save_prize_picture

router = APIRouter(
    prefix="/v1", tags=['prize']
)


@router.get('/prize/{user_id}')
async def get_prizes(auth: AuthResponse = Depends(require_admin)) -> list[PrizeModel]:
    user: User = await User.get(auth.user_id)
    return [prize.get_model() for prize in await user.get_prizes()]


@router.post('/prize')  # переделать передачу admin_id
async def create_prize(prize: PrizeInfo, auth: AuthResponse = Depends(require_admin)) -> Id:
    prize: Prize = Prize.get_repository(prize)
    try:
        await prize.create()
    except ORMUniqueFieldError:
        raise HTTPException(400, 'One of the model fields does not match the uniqueness property.')
    return Id(id=prize.id)


@router.put('/prize')
async def edit_prize(prize_edit: PrizeEdit, auth: AuthResponse = Depends(require_admin)):
    prize: Prize = await Prize.get(prize_edit.id)
    await prize.modify(prize_edit.name, prize_edit.description,
                       prize_edit.icon_link)


@router.delete('/prize')
async def delete_prize(prize_id: Id, auth: AuthResponse = Depends(require_admin)):
    prize: Prize = await Prize.get(prize_id)
    try:
        await prize.delete()
    except ORMRelationError:
        raise HTTPException(400, f'You can not delete {prize} because of relation to another table.')


@router.post("/prize/upload")
async def upload_prize_icon(prize_id: Id, file: UploadFile = File(...), auth: AuthResponse = Depends(require_admin)):
    icon_link = save_prize_picture(prize_id, file.file, file.filename)
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type {file.content_type}"
        )
    if icon_link is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload file.")
    return icon_link
