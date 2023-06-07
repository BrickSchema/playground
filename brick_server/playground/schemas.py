from enum import Enum
from typing import Dict

from brick_server.minimal.schemas import Domain, StrEnumMixin, User
from pydantic import BaseModel, Field


class PermissionProfile(BaseModel):
    class Config:
        orm_mode = True

    read: str = Field(..., description="Read template of the profile")
    write: str = Field(..., description="Write template of the profile")


class PermissionModel(StrEnumMixin, Enum):
    INTERSECTION = "intersection"
    AUGMENTATION = "augmentation"


class App(BaseModel):
    class Config:
        orm_mode = True

    name: str = Field(..., description="Name of the app")
    description: str = Field("", description="")
    approved: bool = Field(False, description="")
    # profile = ReferenceField(PermissionProfile, required=True)


class AppCreate(BaseModel):
    name: str = Field(..., description="Name of the app")
    description: str = Field("", description="")
    profile: PermissionProfile = Field(..., description="")


class DomainUserApp(BaseModel):
    class Config:
        orm_mode = True

    domain: Domain = Field(...)
    user: User = Field(...)
    app: App = Field(...)
    running: bool = Field(False)
    arguments: Dict[str, str]


class DomainUserAppStart(BaseModel):
    arguments: Dict[str, str] = Field({})
