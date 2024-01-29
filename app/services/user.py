from app.db.repository import User
from app.minio.base import upload_file_to_s3
from app.core import config
import urllib.parse


async def save_profile_picture(user_id, file, file_name):
    icon_link = await upload_file_to_s3(file, file_name, "user")
    new_icon_link = urllib.parse.urljoin(config.MINIO_URL, icon_link)
    user: User = await User.get(user_id)
    await user.modify(user.name, new_icon_link)


async def get_user_profile(user_id: int):
    user: User = await User.get(user_id)
    user.icon_link = urllib.parse.urljoin(config.MINIO_URL, user.icon_link)
    return user
