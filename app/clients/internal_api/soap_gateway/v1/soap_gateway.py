from app.clients.base import BaseAPI
from app.core import config


__all__ = [
    "SoapGatewayAPI",
]


class SoapGatewayAPI(BaseAPI):
    """
    Микросервис: `soap_gateway`
    Версия: v1
    """

    base_url: str = config.SOAP_GATEWAY_SERVICE_URL

    @classmethod
    async def soap_method(cls):
        pass
