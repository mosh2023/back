from typing import Callable

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.db.events import init_db


def create_start_app_handler(app: FastAPI, **kwargs) -> Callable:
    from_meta = kwargs.get("from_meta", False)

    async def start_app() -> None:
        await init_db(from_meta=from_meta)
        Instrumentator().instrument(app).expose(app)

    return start_app


def create_stop_app_handler(app: FastAPI, **kwargs) -> Callable:
    async def stop_app() -> None:
        pass

    return stop_app
