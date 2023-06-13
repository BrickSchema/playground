from enum import Enum
from typing import Dict, List

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
    status: str = Field("")
    container_id: str = Field("")
    arguments: Dict[str, str] = Field({})


class DomainUserAppCreate(BaseModel):
    arguments: Dict[str, str] = Field({})
    start: bool = Field(True)


class DockerStatus(StrEnumMixin, Enum):
    """
    The states defined in docker documentation (https://docs.docker.com/engine/reference/commandline/ps/)
    """

    CREATED = "created"
    RESTARTING = "restarting"
    RUNNING = "running"
    REMOVING = "removing"
    PAUSED = "paused"
    EXITED = "exited"
    DEAD = "dead"


class AuthorizedEntities(BaseModel):
    read: List[str] = Field(...)
    write: List[str] = Field(...)
    is_admin: bool = Field(False)
