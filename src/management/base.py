from typing import TypeVar

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now

from src.management.database.manager import BaseManager, ValidManager, DeletedManager
from utils.exception_classes import ObjectDoesNotExist

Base = declarative_base()

T = TypeVar("T", bound=Base)


class BaseModel(Base):
    """
    Base model class for SQLAlchemy models.
    Attributes:
        created (DateTime): The timestamp for when the record was created.
        updated (DateTime): The timestamp for when the record was last updated.
    Usage:
        Subclass this BaseModel when creating SQLAlchemy models to include
        'created' and 'updated' timestamp columns.
    """

    __abstract__ = True
    is_deleted = Column(Boolean, default=False)
    created = Column(DateTime(timezone=True), nullable=False, default=now(), index=True)
    updated = Column(
        DateTime(timezone=True),
        nullable=False,
        default=now(),
        onupdate=now(),
        index=True,
    )

    DoesNotExist = ObjectDoesNotExist

    @classmethod
    @property
    def objects(cls):
        return BaseManager(cls)

    @classmethod
    @property
    def valid_objects(cls):
        return ValidManager(cls)

    @classmethod
    @property
    def deleted_objects(cls):
        return DeletedManager(cls)

    def save(self, action='updated', actor_id=None):
        return self.objects.save(self)

    def delete(self):
        return self.objects.delete(id=self.id)

    @property
    def get_created_at(self):
        return str(self.created)
