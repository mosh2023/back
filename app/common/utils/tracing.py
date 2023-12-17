from typing import Any
import re
import traceback

from medsi_fastapi.tracing import get_tracer
from medsi_fastapi.tracing import TracingIdentifiers
from opentelemetry.trace.status import Status
from opentelemetry.trace.status import StatusCode
import httpx


async def traced_request(
    *args: Any, trid: TracingIdentifiers, **kwargs: Any
) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        if kwargs.get("headers"):
            kwargs["headers"].update(trid.as_headers())
        else:
            kwargs["headers"] = trid.as_headers()

        response = await client.request(*args, **kwargs)
    return response


def format_traceback(e: Exception, cid: str) -> str:
    return "".join(
        re.sub(r"(\n)(?!$)", f"\n{cid} ", re.sub(r"^", cid, line))
        for line in (traceback.format_tb(e.__traceback__))
    )


def mark_exception(span, exc) -> None:
    span.record_exception(exc)
    span.set_status(Status(StatusCode.ERROR))


tracer = get_tracer()
