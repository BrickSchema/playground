from beanie import PydanticObjectId
from sbos.minimal.schemas.base import BaseModel

from sbos.playground.schemas.permission import PermissionModel, PermissionProfileRead


class AppCreate(BaseModel):
    name: str
    description: str = ""


class AppSubmit(BaseModel):
    # profile: PermissionProfileCreate
    profile_read: str | None = None
    profile_write: str | None = None
    permission_model: PermissionModel | None = None
    arguments: dict[str, str] = {}


class AppRead(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    approved: bool


class AppData(BaseModel):
    permission_profile: PermissionProfileRead | None = None
    permission_model: PermissionModel = PermissionModel.INTERSECTION
    frontend: PydanticObjectId | None = None
    backend: PydanticObjectId | None = None


class AppReadWithApprovedData(AppRead):
    approved_data: AppData | None = None


class AppReadWithAllData(AppReadWithApprovedData):
    submitted_data: AppData | None = None


class AppBuild(BaseModel):
    stdout: str
    stderr: str
    returncode: int
