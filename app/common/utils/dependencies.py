from fastapi import Request
from medsi_fastapi.logging_factory import log_service_request as lib_log_service_request

from app.core.logging import logger_factory


async def log_service_request_dependency(request: Request):
    await lib_log_service_request(request, logger_factory)
