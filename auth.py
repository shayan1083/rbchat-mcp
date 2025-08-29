from fastapi import Depends, APIRouter, HTTPException, status, Response
from settings import Settings

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import jwt

settings = Settings()

router = APIRouter()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            scheme, _, token = auth_header.partition(" ")
            if scheme.lower() == "bearer":
                try:
                    payload = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=[settings.ALGORITHM]
                    )
                    request.state.user = payload.get("sub")  # Store user info
                    request.state.token = token
                except jwt.PyJWTError:
                    raise HTTPException(status_code=401, detail="Invalid token")
            else:
                raise HTTPException(status_code=401, detail="Invalid auth scheme")
        else:
            request.state.user = None  # Optional: allow anonymous access
            request.state.token = None

        return await call_next(request)