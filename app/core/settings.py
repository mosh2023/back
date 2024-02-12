from functools import lru_cache
from dotenv import load_dotenv
from os import environ as env
from pydantic_settings import BaseSettings
import logging


load_dotenv()


class AppSettings(BaseSettings):
    LOG_LEVEL: int = logging.DEBUG
    DEBUG: bool = False

    GAME_KEY_LENGTH: int = 6
 
    POSTGRES_USER: str = env.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = env.get('POSTGRES_PASSWORD')
    POSTGRES_PORT: str = env.get('POSTGRES_PORT')
    POSTGRES_HOST: str = env.get('POSTGRES_HOST')
    POSTGRES_DB: str = env.get('POSTGRES_DB')

    POSTGRES_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    MINIO_ACCESS_KEY: str = env.get('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = env.get('MINIO_SECRET_KEY')
    MINIO_HOST: str = env.get('MINIO_HOST')
    MINIO_PORT: str = env.get('MINIO_PORT', '9000')
    MINIO_SECURE: bool = env.get('MINIO_SECURE', 'False') == 'True'

    MINIO_URL: str = f'http://{MINIO_HOST}:{MINIO_PORT}/' \
        if not MINIO_SECURE else f'https://{MINIO_HOST}:{MINIO_PORT}'

    SECRET_KEY: str = env.get('SECRET_KEY')
    ALGORITHM: str = env.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env.get('ACCESS_TOKEN_EXPIRE_MINUTES')


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()
