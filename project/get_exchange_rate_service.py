import datetime
from typing import Optional

import httpx
from pydantic import BaseModel


class GetExchangeRateResponse(BaseModel):
    """
    Response model containing the exchange rate between the specified currencies, along with relevant metadata.
    """

    source_currency: str
    target_currency: str
    exchange_rate: float
    timestamp: str
    conversion_margin: Optional[float] = None


async def get_exchange_rate(
    source_currency: str, target_currency: str
) -> GetExchangeRateResponse:
    """
    Retrieves the current exchange rate between two specified currencies by querying an external API.

    Note: For the sake of this example, the external API URL and the API key are assumed to be predefined constants.

    Args:
        source_currency (str): The ISO currency code (e.g., USD) of the source currency.
        target_currency (str): The ISO currency code (e.g., EUR) of the target currency.

    Returns:
        GetExchangeRateResponse: Response model containing the exchange rate between the specified currencies, along with relevant metadata.
    """
    EXCHANGE_RATES_API_URL = "https://api.exchangerate-api.com/v4/latest/"
    request_url = f"{EXCHANGE_RATES_API_URL}{source_currency}"
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        response.raise_for_status()
        data = response.json()
        exchange_rate = data["rates"][target_currency]
        timestamp = datetime.datetime.now().isoformat()
        conversion_margin = data.get("conversion_margin", None)
        return GetExchangeRateResponse(
            source_currency=source_currency,
            target_currency=target_currency,
            exchange_rate=exchange_rate,
            timestamp=timestamp,
            conversion_margin=conversion_margin,
        )
