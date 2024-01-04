from functools import lru_cache
from dotenv import load_dotenv
from os import environ as env
from pydantic_settings import BaseSettings
import logging


load_dotenv()


class AppSettings(BaseSettings):
    LOG_LEVEL: int = logging.DEBUG

    DEBUG: bool = False
 
    POSTGRES_USER: str = env.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = env.get('POSTGRES_PASSWORD')
    POSTGRES_PORT: str = env.get('POSTGRES_PORT')
    POSTGRES_HOST: str = env.get('POSTGRES_HOST')
    POSTGRES_DB: str = env.get('POSTGRES_DB')

    POSTGRES_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}' \
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'



@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()
