import urllib.parse
import uuid

from app.db.repository import Prize
from app.minio.base import upload_file_to_s3
from app.core import config


async def save_prize_picture(prize_id, file):
    file_extension = file.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    icon_link = await upload_file_to_s3(file.file, file_name, "prize")
    if icon_link is None:
        return None
    new_icon_link = urllib.parse.urljoin('http://localhost:9000/', icon_link)
    prize: Prize = await Prize.get(prize_id)
    await prize.modify(icon_link=new_icon_link)
    return new_icon_link


async def get_prize_info(prize_id: int):
    prize: Prize = await Prize.get(prize_id)
    prize.icon_link = urllib.parse.urljoin(config.MINIO_URL, prize.icon_link)
    return prize
