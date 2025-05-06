from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import BaseModel

from sbos.playground.models.permission import PermissionProfile
from sbos.minimal.models.user import User
from sbos.playground.schemas.permission import PermissionModel


class AppData(BaseModel):
    permission_profile: Link[PermissionProfile] | None = None
    permission_model: PermissionModel = PermissionModel.INTERSECTION
    frontend: PydanticObjectId | None = None
    backend: PydanticObjectId | None = None


class App(Document):
    name: Indexed(str, unique=True)
    description: str = ""
    developer: Link[User] | None = None
    approved: bool = False
    updated: bool = False
    approved_data: AppData | None = None
    submitted_data: AppData | None = None

    class Settings:
        name = "apps"
