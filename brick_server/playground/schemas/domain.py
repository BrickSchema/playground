from beanie import PydanticObjectId
from brick_server.minimal.schemas.base import BaseModel
from brick_server.minimal.schemas.domain import DomainRead
from brick_server.minimal.schemas.user import UserRead

from brick_server.playground.schemas.app import AppRead
from brick_server.playground.schemas.permission import PermissionProfileRead


class DomainAppRead(BaseModel):
    id: PydanticObjectId
    domain: DomainRead
    app: AppRead


class DomainUserRead(BaseModel):
    id: PydanticObjectId
    domain: DomainRead
    user: UserRead
    is_admin: bool = False


class DomainUserAppArguments(BaseModel):
    arguments: dict[str, str] = {}


class DomainUserAppCreate(BaseModel):
    arguments: dict[str, str]
    start: bool = True


class DomainUserAppRead(BaseModel):
    id: PydanticObjectId
    domain: DomainRead
    user: UserRead
    app: AppRead
    status: str
    container_id: str
    arguments: dict[str, str]
    token: str


class DomainUserProfileRead(BaseModel):
    id: PydanticObjectId
    domain: DomainRead
    user: UserRead
    profile: PermissionProfileRead
    arguments: dict[str, str]


class DomainUserProfileCreate(BaseModel):
    profile: PydanticObjectId
    arguments: dict[str, str] = {}


class DomainUserProfileUpdate(BaseModel):
    arguments: dict[str, str]


class DomainPreActuationPolicyCreate(BaseModel):
    name: str
    query: str = ""
    priority: int = 0
    guards: list[str] = []


class DomainPreActuationPolicyRead(BaseModel):
    id: PydanticObjectId
    domain: DomainRead
    name: str
    query: str
    priority: int
    guards: list[str]


class DomainPreActuationPolicyUpdate(BaseModel):
    name: str | None = None
    query: str | None = None
    priority: int | None = None
    guards: list[str] | None = None
