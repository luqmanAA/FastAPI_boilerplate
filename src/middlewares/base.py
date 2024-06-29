from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.utils.storage_backend import storage


class BaseUrlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Set the base URL as a global variable
        if storage.BASE_URL != str(request.base_url):
            setattr(storage, 'BASE_URL', str(request.base_url))

        response = await call_next(request)
        return response
