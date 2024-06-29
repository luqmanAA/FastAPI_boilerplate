import traceback

from src.utils.response_classes import CJSONResponse
from src.utils.schemas import ResponseSchema


def exception_handler_base(request, exc, success=False, msg=None, status_code=500):
    message = "Something went wrong"

    if str(status_code).startswith('5'):
        print(traceback.format_exc())
        exc = "Internal server error"
        message = "It's not you it's us, our engineers are working on it"
    response = ResponseSchema(
        success=success,
        message=message,
        errors=exc
    ).dict()

    return CJSONResponse(status_code=status_code, content=response)
