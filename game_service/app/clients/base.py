from functools import partial
from typing import Any
from typing import Literal
from typing import Optional
from typing import Tuple
import json

from aiohttp import ClientResponse
from aiohttp import ClientTimeout
from aiohttp import ContentTypeError
from fastapi import status as HTTPStatus
from medsi_fastapi.logging_factory import LogHandler
from medsi_fastapi.tracing import TracingIdentifiers

from app.clients.exceptions import BadRequestAPIException
from app.clients.exceptions import ClientErrorAPIException
from app.clients.exceptions import ServerErrorAPIException
from app.common.utils.logging import JSONCustomEncoder
from app.common.utils.session import RetryClientSession
from app.common.utils.tracing import tracer
from app.core import config
from app.core.logging import logger_factory


__all__ = ("BaseAPI",)

request_logger = logger_factory.get_logger(LogHandler.HTTP_REQUEST)
response_logger = logger_factory.get_logger(LogHandler.HTTP_RESPONSE)


class BaseAPI:
    base_url: Optional[str] = None

    @classmethod
    async def request(
        cls,
        method: Literal["get", "post", "put", "patch", "delete", "options"],
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
        retry_client_session_params: Optional[dict] = None,
        verify_ssl: bool = True,
    ) -> Tuple[int, Any]:
        if not retry_client_session_params:
            retry_client_session_params = {}

        _url = f"{cls.base_url}{path}"
        with tracer.start_as_current_span(f"BaseAPI.request: {_url}") as span:
            _headers = {
                "Content-Type": "application/json",
                "service-name": config.PROJECT_NAME,
            }
            if span.is_recording():
                _headers.update(TracingIdentifiers.from_span(span).as_headers())

            if headers:
                _headers.update(headers)

            _params = params or {}
            _json = body or {}

            async with RetryClientSession(
                json_serialize=partial(json.dumps, cls=JSONCustomEncoder),
                timeout=ClientTimeout(
                    total=20,
                ),
                **retry_client_session_params,
            ) as session:
                response: ClientResponse
                _session_method = getattr(session, method)
                span.add_event(
                    "Request",
                    attributes=dict(
                        method=method,
                        path=path,
                        url=_url,
                        headers=str(_headers),
                        params=str(_params),
                        json=str(_json),
                    ),
                )
                await request_logger.info(
                    request_method=method,
                    request_url=_url,
                    request_headers=_headers,
                    request_params=params,
                    request_body=_json,
                )
                async with _session_method(
                    url=_url,
                    headers=_headers,
                    params=_params,
                    json=_json,
                    verify_ssl=verify_ssl,
                ) as response:
                    try:
                        response_json = await response.json()
                    except ContentTypeError:
                        response_json = {}

                    span.add_event(
                        "Response",
                        attributes=dict(
                            response_status=response.status,
                            response_text=str(response_json),
                        ),
                    )

            if response.status == HTTPStatus.HTTP_400_BAD_REQUEST:
                await response_logger.error(
                    response_status=response.status,
                    response_body=response_json,
                )
                raise BadRequestAPIException(
                    response.status,
                    response_json.get("detail"),
                )
            elif (
                HTTPStatus.HTTP_400_BAD_REQUEST
                < response.status
                <= HTTPStatus.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            ):
                await response_logger.error(
                    response_status=response.status,
                    response_body=response_json,
                )
                raise ClientErrorAPIException(
                    response.status,
                    response_json.get("detail"),
                )
            elif response.status >= HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR:
                await response_logger.error(
                    response_status=response.status,
                    response_body=response_json,
                )
                raise ServerErrorAPIException(response.status, response._body)
            else:
                await response_logger.info(
                    response_status=response.status,
                    response_body=response_json,
                )

            return response.status, response_json

    @classmethod
    async def get_alive(cls) -> Tuple[int, Any]:
        status_code, response = 0, {}  # type: ignore

        try:
            status_code, response = await cls.request(
                method="get",
                path="/live",
            )
        except (
            ClientErrorAPIException,
            BadRequestAPIException,
            ServerErrorAPIException,
        ) as e:
            status_code = e.status_code

        return status_code, response
