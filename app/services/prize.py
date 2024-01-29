import urllib.parse

from app.db.repository import Prize
from app.minio.base import upload_file_to_s3
from app.core import config


async def save_prize_picture(prize_id, file, file_name):
    icon_link = await upload_file_to_s3(file, file_name, "prize")
    new_icon_link = urllib.parse.urljoin(config.MINIO_URL, icon_link)
    prize: Prize = await Prize.get(prize_id)
    await prize.modify(prize.name, new_icon_link)


async def get_prize_info(prize_id: int):
    prize: Prize = await Prize.get(prize_id)
    prize.icon_link = urllib.parse.urljoin(config.MINIO_URL, prize.icon_link)
    return prize
