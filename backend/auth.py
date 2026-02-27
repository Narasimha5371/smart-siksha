from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings
import secrets

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if not secrets.compare_digest(api_key, settings.API_AUTH_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return api_key
