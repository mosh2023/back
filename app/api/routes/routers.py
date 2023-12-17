from typing import Callable

from fastapi import Request
from fastapi import Response
from fastapi.routing import APIRoute


class RequestLoggingRouter(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            raw_body = await request.body()
            body = raw_body.decode(encoding="latin-1")
            request.app.logger.info(
                f"Processing request to {request.url}"
                f" | {request.method}"
                f" | {request.headers}"
                f" | {request.cookies}"
                f" | {request.client}"
                f" | {body=}"
            )
            response = await original_route_handler(request)

            return response

        return custom_route_handler
