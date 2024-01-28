import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import v1_routers, mock_routers

logging.getLogger("charset_normalizer").disabled = True


def get_application() -> FastAPI:
    app: FastAPI = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    # for router in mock_routers:
    #     app.include_router(router)

    for router in v1_routers:
        app.include_router(router)

    return app


app = get_application()
