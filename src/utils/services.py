from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from src.utils.get_objects import Paginator
from src.utils.schemas import ResponseSchema, PageFilter, PaginatedResponse


class GenericCRUDService:
    def __init__(self, model):
        self.model = model

    def get_queryset(self, user, search_kwargs: dict = None, **kwargs):
        return self.model.valid_objects.filter_query(**kwargs, search_kwargs=search_kwargs)


    def get_object(self, request: Request, obj_id: int):
        try:
            return self.model.valid_objects.get(id=obj_id)

        except self.model.DoesNotExist:
            raise HTTPException(status_code=404)

    def create(
            self, request, payload, out_schema: BaseModel
    ) -> ResponseSchema[Union[dict]]:
        # payload.update({'created_by_id': request.user.id})
        obj = self.model.valid_objects.create(**payload)
        return ResponseSchema(
            success=True,
            data=out_schema.model_validate(obj).model_dump(),
            message="Item created successfully",
        )

    def get(
            self, request: Request, obj_id: int, out_schema: BaseModel
    ) -> ResponseSchema:
        obj = self.get_object(request, obj_id)

        return ResponseSchema(
            success=True,
            data=out_schema.model_validate(obj).model_dump(),
            message="Data retrieved successfully",
        )

    def filter_queryset(self, request: Request, page_filter: PageFilter, search_kwargs: dict = None):
        filters = page_filter.dict()
        filters = {
            key: value for key, value in filters.items()
            if value is not None and key not in PageFilter().dict()
        }
        if filters:
            return self.get_queryset(request.user, search_kwargs=search_kwargs, **filters)

        return self.get_queryset(request.user, search_kwargs=search_kwargs)

    def list(
            self,
            request: Request,
            page_filter: PageFilter,
            response_schema: BaseModel,
            role_id=None,
            search_kwargs: dict = None
    ):
        queryset = self.filter_queryset(request, page_filter, search_kwargs=search_kwargs)

        return self.paginated_list(request, queryset, page_filter, response_schema)

    def paginated_list(self, request, queryset, page_filter, response_schema):
        page = Paginator(
            model=self.model,
            queryset=queryset,
            request=request,
            per_page=page_filter.page_size,
        )
        response = PaginatedResponse(
            **page.get_page(page_filter.page_index),
            results=[response_schema.from_orm(item).dict() for item in page.object_list()]
        )

        return ResponseSchema(
            success=True,
            data=response,
            message="Data retrieved successfully",
        )

    def unpaginated_list(
            self,
            request: Request,
            page_filter: None | PageFilter,
            response_schema: BaseModel,
            search_kwargs: dict = None
    ):

        queryset = self.filter_queryset(request, page_filter, search_kwargs)

        return ResponseSchema(
            success=True,
            data=[response_schema.from_orm(item).dict() for item in queryset],
            message="Data retrieved successfully",
        )

    def update(
            self, request: Request, obj_id: int, payload, out_schema: BaseModel
    ) -> ResponseSchema[Union[dict]]:
        obj = self.get_object(request, obj_id)
        self.model.valid_objects.update(id=obj.id, data=payload)

        return ResponseSchema(
            success=True,
            data=out_schema.model_validate(obj).model_dump(),
            message="Data updated successfully",
        )

    def delete(self, request: Request, obj_id: int) -> ResponseSchema:
        obj = self.get_object(request, obj_id)
        obj.delete()
        return ResponseSchema(
            success=True,
            message="Data deleted successfully",
        )
