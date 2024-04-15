from typing import Optional

import httpx
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetIpGeolocationResponse(BaseModel):
    """
    Response model for IP geolocation data.
    """

    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    isp: str
    organization: Optional[str] = None


async def get_ip_geolocation(ip: str) -> GetIpGeolocationResponse:
    """
    Retrieves geolocation data for a given IP address by querying an external geolocation service.

    Args:
    ip (str): The IP address for which geolocation data is requested.

    Returns:
    GetIpGeolocationResponse: Response model for IP geolocation data.

    The function queries the 'ip-api.com' service to retrieve geolocation data for a specified IP address.
    The retrieved data includes country, region, city, latitude, longitude, ISP, and organization information.
    """
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        await prisma.models.Request.prisma().create(
            data={
                "userId": "placeholder_user_id",
                "endpoint": "get_ip_geolocation",
                "status": prisma.enums.RequestStatus.Success
                if response.status_code == 200
                else prisma.enums.RequestStatus.Failure,
                "response": str(data),
            }
        )
        return GetIpGeolocationResponse(
            country=data.get("country"),
            region=data.get("regionName"),
            city=data.get("city"),
            latitude=data.get("lat"),
            longitude=data.get("lon"),
            isp=data.get("isp"),
            organization=data.get("org"),
        )
