import logging

from fastapi import FastAPI
# from fastapi import Depends
# from fastapi import HTTPException
# from fastapi.exceptions import RequestValidationError
# from starlette.middleware.base import BaseHTTPMiddleware

# from game_service.app.api import probs_router
# from game_service.app.api import service_router
# from app.common.utils.dependencies import log_service_request_dependency
from app.core import config
# from app.core.events import create_start_app_handler
# from app.core.events import create_stop_app_handler
# from app.core.middleware import exception_handle_middleware
# from app.core.middleware import log_service_response

from api.routes import mock_routers


logging.getLogger("charset_normalizer").disabled = True


def get_application() -> FastAPI:
    app: FastAPI = FastAPI()

    # app.add_middleware(BaseHTTPMiddleware, dispatch=exception_handle_middleware)
    # app.add_middleware(BaseHTTPMiddleware, dispatch=log_service_response)

    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)

    # app.add_event_handler("startup", create_start_app_handler(app))
    # app.add_event_handler("shutdown", create_stop_app_handler(app))

    # application.include_router(probs_router, tags=["Probs"])
    # application.include_router(
    #     service_router,
    #     prefix=config.API_ROUTE,
    #     dependencies=[Depends(log_service_request_dependency)],
    # )

    for router in mock_routers:
        app.include_router(router)

    return app


app = get_application()
