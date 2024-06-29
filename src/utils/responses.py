from typing import Any, Union, List, Dict

from src.utils.schemas import ResponseSchema


class ResponseType:
    @staticmethod
    def validation_error(errors: Any, message: str = "Something went wrong"):
        response_data = ResponseSchema(
            success=False, errors=errors, message=message
        )

        return 400, response_data

    @staticmethod
    def response_with_data(
        data: Union[List, Dict],
        status_code: int = 200,
        message: str = "Operation Successful",
    ):
        if status_code == 201:
            message = "Item created successfully"

        response_data = ResponseSchema(
            success=True, data=data, message=message
        )

        return status_code, response_data


responseType = ResponseType()


STATUS_CODES = frozenset({200, 400, 201, 401})
