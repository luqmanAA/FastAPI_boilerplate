from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from src.management.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # @property
    # def get_profile_img(self):
    #     if self.profile_image:
    #         return urljoin(storage.media_storage, self.profile_image)
    #     return None

