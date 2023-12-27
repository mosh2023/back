import logging

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from medsi_fastapi.app import MedsiFastApi
from medsi_fastapi.app import SentryConfig
from medsi_fastapi.app import TracingConfig
from medsi_fastapi.errors.errors.http import http_error_handler
from medsi_fastapi.errors.errors.validation import http422_error_handler
from starlette.middleware.base import BaseHTTPMiddleware

from game_service.app.api import probs_router
from game_service.app.api import service_router
from app.common.utils.dependencies import log_service_request_dependency
from app.core import config
from app.core.events import create_start_app_handler
from app.core.events import create_stop_app_handler
from app.core.middleware import exception_handle_middleware
from app.core.middleware import log_service_response


logging.getLogger("charset_normalizer").disabled = True


def get_application() -> FastAPI:
    if config.TRACING:
        tracing_config = TracingConfig(
            host=config.JAEGER_AGENT,
            port=config.JAEGER_AGENT_PORT,
            name=config.PROJECT_NAME,
        )
    else:
        tracing_config = None  # type: ignore

    if config.SENTRY_DSN:
        sentry_config = SentryConfig(
            dsn=config.SENTRY_DSN,
            environment=config.ENV,
        )
    else:
        sentry_config = None  # type: ignore

    application: FastAPI = MedsiFastApi.build(
        title=config.PROJECT_NAME,
        description=f"API сервиса {config.PROJECT_NAME}",
        root_path=config.API_ROOT_PATH,
        version=config.VERSION,
        debug=config.DEBUG,
        tracing=tracing_config,
        metrics=None,
        sentry=sentry_config,
    )

    application.add_middleware(BaseHTTPMiddleware, dispatch=exception_handle_middleware)
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_service_response)

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(probs_router, tags=["Probs"])
    application.include_router(
        service_router,
        prefix=config.API_ROUTE,
        dependencies=[Depends(log_service_request_dependency)],
    )

    return application


app = get_application()
