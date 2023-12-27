from typing import Any
import re
import traceback

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from medsi_fastapi.log_records.base_record import set_up_correlation_id
from medsi_fastapi.logging_factory import (
    log_service_response as lib_log_service_response,
)
import sentry_sdk

from app.core import config
from app.core.logging import logger_factory


logger = logger_factory.get_logger()


async def exception_handle_middleware(request: Request, call_next: Any) -> Any:
    """Метод для обработки исключений,\n
    которые не обрабатываются установленными через `FastAPI.add_exception_handler` обработчиками.\n
    """
    try:
        return await call_next(request)
    except Exception as exc:
        if not exc.args:
            exc.args = (exc.__class__.__name__,)

        traceback_message = " -> ".join(
            [
                re.sub(r"\n[\s]{4}", " | ", line.strip())
                for line in traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                )[-5:]
            ]
        )
        await logger.error(
            message="Exception middleware",
            traceback_message=traceback_message,
            exception=str(exc),
        )

        if config.SENTRY_DSN:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", dict(request))
                sentry_sdk.capture_exception(exc)

        if config.DEBUG:
            return PlainTextResponse(
                status_code=500,
                content="".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                ),
            )

        return JSONResponse(
            status_code=500,
            content={"message": "Something went wrong. For details see service logs."},
        )


async def log_service_response(request, call_next):
    set_up_correlation_id()
    response = await lib_log_service_response(request, call_next, logger_factory)
    return response
