from datetime import datetime, date
from typing import List, TypeVar, Generic, Optional, Union

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel


GenericResultsType = TypeVar("GenericResultsType")


class BaseSchema(BaseModel):

    class Config:
        from_attributes = True


class BaseReadSchema(BaseSchema):
    created_at: datetime = Field(alias='created')
    updated_at: datetime = Field(alias='updated')


class PageFilter(BaseModel):
    page_index: int = 1
    page_size: int = 10


class BaseFilter(PageFilter):
    date_from: date | datetime | None = None
    date_to: date | datetime | None = None


class BaseSearchSchema(PageFilter):
    search: str | None = None


# class PaginatedResponse(BaseModel):
#     count: int | None = 0
#     next: str | None
#     previous: str | None
#     total_count: int | None = 0
#     page: int
#     page_size: int

class PaginatedResponse(GenericModel, Generic[GenericResultsType]):
    count: int | None = 0
    next: str | None
    previous: str | None
    total_count: int | None = 0
    total_page: int | None = 0
    page_index: int
    page_size: int
    results: List[GenericResultsType]

    class Config:
        arbitrary_types_allowed = True


class ResponseSchema(GenericModel, Generic[GenericResultsType]):
    data: Optional[GenericResultsType]
    success: bool = True
    errors: Optional[Union[str, list, dict]]
    message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


def bad_response(error: str, status_code: int = 404):
    try:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "errors": error,
            },
        )
    except Exception as e:
        print(str(e))
