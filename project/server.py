import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.generate_qr_code_service
import project.get_exchange_rate_service
import project.get_ip_geolocation_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="q2",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit serves as an all-encompassing suite of API endpoints, aimed at simplifying the integration process for developers by providing a wide array of functionalities within a single toolkit. This comprehensive toolkit eliminates the need for multiple third-party services by including essential features such as QR Code Generation for swift information sharing, Currency Exchange Rates for real-time financial data, IP Geolocation for precise location tracking, Image Resizing for dynamic media adjustment, Password Strength Checker for security enhancement, Text-to-Speech for natural audio output, Barcode Generation for various format support, Email Validation for ensuring deliverability, Time Zone Conversion for accurate global timing, URL Preview for link metadata extraction, PDF Watermarking for document customization, and RSS Feed to JSON for seamless content transformation into structured data. It is designed to be straightforward and user-friendly, catering to a broad spectrum of developer needs in a single, efficient package.",
)


@app.post(
    "/qr-code/generate",
    response_model=project.generate_qr_code_service.GenerateQRCodeResponse,
)
async def api_post_generate_qr_code(
    content: str,
    size: str,
    encoding: Optional[str],
    error_correction: Optional[str],
    border: Optional[int],
) -> project.generate_qr_code_service.GenerateQRCodeResponse | Response:
    """
    Generates a QR code based on specified data and customization options.
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            content, size, encoding, error_correction, border
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/currency/exchange-rate",
    response_model=project.get_exchange_rate_service.GetExchangeRateResponse,
)
async def api_get_get_exchange_rate(
    source_currency: str, target_currency: str
) -> project.get_exchange_rate_service.GetExchangeRateResponse | Response:
    """
    Retrieves the current exchange rate between two specified currencies.
    """
    try:
        res = await project.get_exchange_rate_service.get_exchange_rate(
            source_currency, target_currency
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/ip-geolocation/{ip}",
    response_model=project.get_ip_geolocation_service.GetIpGeolocationResponse,
)
async def api_get_get_ip_geolocation(
    ip: str,
) -> project.get_ip_geolocation_service.GetIpGeolocationResponse | Response:
    """
    Retrieves geolocation data for a given IP address.
    """
    try:
        res = await project.get_ip_geolocation_service.get_ip_geolocation(ip)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
