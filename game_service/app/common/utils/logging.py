from datetime import date
from datetime import datetime
from decimal import Decimal
from enum import Enum
from functools import wraps
from typing import Any
from typing import Callable
import inspect
import json
import uuid

from app.core.logging import logger_factory


logger = logger_factory.get_logger()


def background_task_logging_wrapper(func: Callable) -> Callable:
    task_name = func.__name__

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> None:
        task_id = uuid.uuid4()

        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join("{}={!r}".format(*item) for item in func_args.items())

        await logger.info(
            message="Task started",
            task_id=task_id,
            task_name=task_name,
            func_args_str=func_args_str,
        )

        try:
            await func(*args, **kwargs)
            await logger.info(
                message="Task finished successfully",
                task_id=task_id,
                task_name=task_name,
            )
        except Exception as e:
            await logger.error(
                message="Failed permanently with error",
                task_id=task_id,
                task_name=task_name,
                exception=str(e),
            )

    return wrapper


class JSONCustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
