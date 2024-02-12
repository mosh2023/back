import uuid
from urllib.parse import urlparse, urlunparse

from app.core import config
from app.db.repository import User
from app.minio.base import upload_file_to_s3


async def save_profile_picture(user_id, file):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    icon_link = await upload_file_to_s3(file.file, file_name, "user")
    if icon_link is None:
        return None

    parsed_url = urlparse(icon_link)

    new_netloc = f"localhost:{config.MINIO_PORT}"
    new_parsed_url = parsed_url._replace(netloc=new_netloc)
    new_icon_link = str(urlunparse(new_parsed_url))

    user: User = await User.get(user_id)
    await user.modify(icon_link=new_icon_link)

    return new_icon_link


async def get_user_profile(user_id: int):
    user: User = await User.get(user_id)

    parsed_url = urlparse(user.icon_link)

    new_netloc = f"localhost:{config.MINIO_PORT}"
    new_parsed_url = parsed_url._replace(netloc=new_netloc)
    user.icon_link = urlunparse(new_parsed_url)

    return user
