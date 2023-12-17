from typing import Any
from typing import Optional

from aiohttp import AsyncResolver
from aiohttp import TCPConnector
from aiohttp_retry import ExponentialRetry
from aiohttp_retry import RetryClient
from aiohttp_retry import RetryOptionsBase
from aiohttp_retry.client import _Logger
from starlette.datastructures import CommaSeparatedStrings

from app.core import config


class RetryClientSession(RetryClient):
    def __init__(
        self,
        logger: Optional[_Logger] = None,
        dns_tries: int = config.HTTP_CLIENT_DNS_MAX_ATTEMPTS,
        dns_timeout: float = config.HTTP_CLIENT_DNS_TIMEOUT,
        http_attempts: int = config.HTTP_CLIENT_MAX_ATTEMPTS,
        http_start_timeout: float = config.HTTP_CLIENT_START_TIMEOUT,
        http_max_timeout: float = config.HTTP_CLIENT_MAX_TIMEOUT,
        http_backoff_factor: float = config.HTTP_CLIENT_BACKOFF_FACTOR,
        http_retry_statuses: Optional[
            CommaSeparatedStrings
        ] = config.HTTP_CLIENT_RETRY_STATUSES,
        raise_for_status: bool = config.HTTP_CLIENT_RAISE_FOR_STATUS,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        status_set = set()
        if http_retry_statuses is not None:
            for status in http_retry_statuses:
                status_set.add(int(status))
        retry_options: RetryOptionsBase = ExponentialRetry(
            attempts=http_attempts,
            start_timeout=http_start_timeout,
            max_timeout=http_max_timeout,
            factor=http_backoff_factor,
            statuses=status_set or None,
        )
        resolver = AsyncResolver(
            tries=dns_tries,
            timeout=dns_timeout,
        )
        tcp_connector = TCPConnector(resolver=resolver)
        kwargs.setdefault("connector", tcp_connector)
        super().__init__(
            logger,
            retry_options,
            raise_for_status,
            *args,
            **kwargs,
        )
