from enum import Enum
from typing import Dict, List, Optional

from brick_server.minimal.schemas import Domain, StrEnumMixin, User
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, Field


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # if not isinstance(v, BsonObjectId):
        #     raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class PermissionProfile(BaseModel):
    class Config:
        orm_mode = True

    id: PydanticObjectId = Field(...)
    read: str = Field(..., description="Read template of the profile")
    write: str = Field(..., description="Write template of the profile")


class PermissionProfileUpdate(BaseModel):
    read: Optional[str] = Field(None, description="Read template of the profile")
    write: Optional[str] = Field(None, description="Write template of the profile")


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
    response_time: float = Field(0)


class NotifyResource(BaseModel):
    location: str = Field(...)
    resource_type: str = Field(...)
    value: float = Field(...)


class DomainPreActuationPolicyCreate(BaseModel):
    name: str = Field(...)
    query: str = Field("")
    priority: int = Field(0)
    guards: List[str] = Field([])


class DomainPreActuationPolicy(DomainPreActuationPolicyCreate):
    class Config:
        orm_mode = True

    domain: Domain = Field(...)
