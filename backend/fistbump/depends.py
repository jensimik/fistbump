from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .auth import authenticated_user, get_current_user
from .config import settings

api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.auth_token:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
