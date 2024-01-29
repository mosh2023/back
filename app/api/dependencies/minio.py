import boto3
from app.core import config

client = boto3.client(
    's3',
    endpoint_url=config.MINIO_URL,
    aws_secret_access_key=config.MINIO_SECRET_KEY,
    aws_access_key_id=config.MINIO_ACCESS_KEY
)
