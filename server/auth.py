from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from server.config import settings

_bearer = HTTPBearer(auto_error=False)


async def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
):
    if not settings.auth_token:
        return

    if not credentials or credentials.credentials != settings.auth_token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
