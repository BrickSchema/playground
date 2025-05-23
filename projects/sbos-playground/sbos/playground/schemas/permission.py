from enum import Enum
from typing import Literal

from beanie import PydanticObjectId
from sbos.minimal.schemas.base import BaseModel, StrEnumMixin


class PermissionModel(StrEnumMixin, Enum):
    INTERSECTION = "intersection"
    AUGMENTATION = "augmentation"


class PermissionProfileCreate(BaseModel):
    name: str
    read: str
    write: str
    arguments: dict[str, str]


class PermissionProfileRead(BaseModel):
    id: PydanticObjectId
    name: str = ""
    type: Literal["app", "user"] = "user"
    read: str
    write: str
    arguments: dict[str, str]


class PermissionProfileUpdate(BaseModel):
    name: str | None = None
    read: str | None = None
    write: str | None = None
    arguments: dict[str, str] | None = None


class AuthorizedEntities(BaseModel):
    read: dict[str, list[str]]
    write: dict[str, list[str]]
    is_admin: bool = False
    response_time: float = 0
