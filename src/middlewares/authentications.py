from starlette.authentication import AuthenticationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.utils.exception_handlers import exception_handler_base


class AuthExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            credentials = await self.app.backend.authenticate(request)
            request.state.credentials = credentials
        except AuthenticationError as exc:
            return exception_handler_base(
                request,
                exc=str(exc),
                status_code=401,
                success=False
            )

        response = await call_next(request)

        return response
