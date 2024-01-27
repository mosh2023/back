import aioboto3
from app.core import config

session = aioboto3.Session(
        aws_access_key_id=config.MINIO_ACCESS_KEY,
        aws_secret_access_key=config.MINIO_SECRET_KEY)
