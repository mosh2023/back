from functools import lru_cache
from typing import List
from typing import Optional

from pydantic_settings import BaseSettings
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings


config = Config("env/.env.test")


class APPSettings(BaseSettings):
    PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="TemplateService")
    VERSION: str = config("VERSION", cast=str, default="1.0.0")

    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    ENV: str = config("ENV", cast=str, default="TEST")

    DATABASE_URL: str = config(
        "DATABASE_URL",
        cast=str,
        default="postgresql+asyncpg://postgres:DT0546/admin@127.0.0.1:5432/db_name",
    )
    print('!' * 30, DATABASE_URL)

    API_ROUTE: str = config("API_ROUTE", cast=str, default="/path")
    API_ROOT_PATH: str = config("API_ROOT_PATH", default="")

    LOGGING_LEVEL: str = config("LOGGING_LEVEL", cast=str, default="INFO")
    LOGGING_SERIALIZE: bool = config("LOGGING_SERIALIZE", cast=bool, default=False)
    LOGGING_USING_CONSOLE: bool = config(
        "LOGGING_USING_CONSOLE", cast=bool, default=True
    )
    LOGGING_USING_GRAYLOG: bool = config(
        "LOGGING_USING_GRAYLOG", cast=bool, default=False
    )
    LOGGING_GRAYLOG_UDP_HOST: str = config(
        "LOGGING_GRAYLOG_UDP_HOST", cast=str, default="devgraylog.medsi.pro"
    )
    LOGGING_GRAYLOG_UDP_PORT: int = config(
        "LOGGING_GRAYLOG_UDP_PORT", cast=int, default=12201
    )

    TRACING: bool = config("TRACING", cast=bool, default=True)
    JAEGER_AGENT: str = config("JAEGER_AGENT", cast=str, default="10.13.6.54")
    JAEGER_AGENT_PORT: int = config("JAEGER_AGENT_PORT", cast=int, default=2031)

    SOAP_GATEWAY_SERVICE_URL: str = config(
        "SOAP_GATEWAY_SERVICE", cast=str, default="localhost"
    )

    HTTP_CLIENT_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_MAX_ATTEMPTS", cast=int, default=3
    )
    HTTP_CLIENT_START_TIMEOUT: float = config(
        "HTTP_CLIENT_START_TIMEOUT", cast=float, default=0.1
    )
    HTTP_CLIENT_MAX_TIMEOUT: float = config(
        "HTTP_CLIENT_MAX_TIMEOUT", cast=float, default=30.0
    )
    HTTP_CLIENT_BACKOFF_FACTOR: float = config(
        "HTTP_CLIENT_BACKOFF_FACTOR", cast=float, default=2.0
    )
    HTTP_CLIENT_DNS_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_DNS_MAX_ATTEMPTS", cast=int, default=4
    )
    HTTP_CLIENT_DNS_TIMEOUT: float = config(
        "HTTP_CLIENT_DNS_TIMEOUT", cast=float, default=5.0
    )
    HTTP_CLIENT_RAISE_FOR_STATUS: bool = config(
        "HTTP_CLIENT_RAISE_FOR_STATUS", cast=bool, default=False
    )
    HTTP_CLIENT_RETRY_STATUSES: Optional[CommaSeparatedStrings] = config(
        "HTTP_CLIENT_RETRY_STATUSES", cast=CommaSeparatedStrings, default=None
    )
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)

    KEYCLOAK_AUTH_URL: str = config(
        "KEYCLOAK_AUTH_URL",
        cast=str,
        default="https://predprod-kong-dev.smartmed.pro/kc/auth/",
    )

    KAFKA_BOOTSTRAP_SERVER: str = config("KAFKA_BOOTSTRAP_SERVER", cast=str, default="")

    SENTRY_DSN: str = config("SENTRY_DSN", cast=str, default="")

    AUTH_ENABLED: bool = config("AUTH_ENABLED", cast=bool, default=False)
    API_KEY_TOKEN: str = config("API_KEY_TOKEN", cast=str, default="")

    class Config:
        env_file = ".env"


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
