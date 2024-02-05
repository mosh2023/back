import urllib.parse
import uuid

from app.core import config
from app.db.repository import User
from app.minio.base import upload_file_to_s3


async def save_profile_picture(user_id, file):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    icon_link = await upload_file_to_s3(file.file, file_name, "user")
    if icon_link is None:
        return None
    new_icon_link = urllib.parse.urljoin(config.MINIO_URL, icon_link)
    user: User = await User.get(user_id)
    await user.modify(user.name, new_icon_link)
    return new_icon_link


async def get_user_profile(user_id: int):
    user: User = await User.get(user_id)
    user.icon_link = urllib.parse.urljoin(config.MINIO_URL, user.icon_link)
    return user
