import uuid
from urllib.parse import urlparse, urlunparse


from app.db.repository import Prize
from app.minio.base import upload_file_to_s3
from app.core import config


async def save_prize_picture(prize_id, file):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    icon_link = await upload_file_to_s3(file.file, file_name, "prize")
    if icon_link is None:
        return None

    parsed_url = urlparse(icon_link)

    new_netloc = f"localhost:{config.MINIO_PORT}"
    new_parsed_url = parsed_url._replace(netloc=new_netloc)
    new_icon_link = str(urlunparse(new_parsed_url))

    prize: Prize = await Prize.get(prize_id)
    await prize.modify(icon_link=new_icon_link)
    return new_icon_link


async def get_prize_info(prize_id: int):
    prize: Prize = await Prize.get(prize_id)

    parsed_url = urlparse(prize.icon_link)

    new_netloc = f"localhost:{config.MINIO_PORT}"
    new_parsed_url = parsed_url._replace(netloc=new_netloc)
    prize.icon_link = urlunparse(new_parsed_url)

    return prize
