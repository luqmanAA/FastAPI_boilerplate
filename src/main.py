from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.authentication import AuthenticationMiddleware

from src.config import ALLOWED_ORIGINS, ALLOWED_METHODS, ALLOWED_HOST
from .authentication.auth import JWTAuthBackend
from .management.base import Base
from .management.settings import DATABASE_URL, DEBUG
from .middlewares.authentications import AuthExceptionMiddleware
from .middlewares.base import BaseUrlMiddleware
from .utils.exception_handlers import exception_handler_base
from .utils.exception_classes import ObjectDoesNotExist
from .utils.response_classes import CJSONResponse

app = FastAPI(
    debug=DEBUG,
    default_response_class=CJSONResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HOST,
)
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(AuthExceptionMiddleware)
app.add_middleware(BaseUrlMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if isinstance(exc.errors(), list):
        try:
            errors = [{item["loc"][-1]: item["msg"]} for item in exc.errors()]
        except:
            errors = exc.errors()

    return exception_handler_base(request, exc=errors, status_code=400)


@app.exception_handler(ValueError)
async def valueerror_exception_handler(request: Request, exc):
    return exception_handler_base(request, str(exc), status_code=400, success=False)


@app.exception_handler(ObjectDoesNotExist)
async def object_not_exists_exception_handler(request: Request, exc):
    return exception_handler_base(
        request, "Item not found", status_code=404,
        success=False
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc):
    return exception_handler_base(request, exc.errors(), status_code=500)


Base.metadata.create_all(bind=engine)
