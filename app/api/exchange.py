from fastapi import APIRouter, Header, HTTPException, Depends
from app.api_clients.exchange import ExchangeApiClient
from app.api_clients.auth import AuthApiClient
from typing import Annotated

from app.utils.logs import get_logger

router = APIRouter()
logger = get_logger(__name__)

exchange_client = ExchangeApiClient.prepare()
auth_client = AuthApiClient.prepare()

# Dependency to verify and extract user from token via Auth service
async def verify_user(token: str = Header(...)):
    try:
        user = await auth_client.get_user(token)
        return user  # Forward user info if needed
    except Exception as e:
        logger.error(f"Error verifying user: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/rate/{currency}")
async def get_currency_rate(
    currency: str,
    user = Depends(verify_user)
):
    try:
        return await exchange_client.get_conversion_rate(currency=currency)
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
        raise HTTPException(status_code=500, detail=str(e))
