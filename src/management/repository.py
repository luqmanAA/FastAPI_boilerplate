from typing import TypeVar, Type

from .base import Base

T = TypeVar("T", bound=Base)


def field_update(obj: Type[T], data_to_update: dict) -> T:
    for key, value in data_to_update.items():
        val = data_to_update[key]
        if val is not None:
            setattr(obj, key, value)
