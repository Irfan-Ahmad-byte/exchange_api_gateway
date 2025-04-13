from app.api_clients.client import ApiClient
from app.configs.configs import settings
from app.utils.logs import get_logger

logger = get_logger(__name__)

class ExchangeApiEndPoints:
    EXCHANGE_CONVERSION = "/rate/{currency}"


class ExchangeApiClient:
    def __init__(self, api_client: ApiClient):
        self.exchange = api_client

    @staticmethod
    def prepare() -> "ExchangeApiClient":
        base_url = settings.EXCHANGE_BASE_URL
        api_key = settings.EXCHANGE_API_KEY
        api_secret = settings.EXCHANGE_API_SECRET

        if not base_url:
            logger.error("Environment variables for EXCHANGE API are missing")
            raise EnvironmentError("Required environment variables are not set.")

        headers = {
            "X-Api-Key": api_key,
            "X-Api-Secret": api_secret
        }

        return ExchangeApiClient(ApiClient(base_url, headers))
    
    def get_conversion_rate(self, currency: str):
        return self.exchange.get(ExchangeApiEndPoints.EXCHANGE_CONVERSION.format(currency=currency), headers=None)