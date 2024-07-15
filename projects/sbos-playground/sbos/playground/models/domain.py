from typing import TYPE_CHECKING

from beanie import Document, Link
from pymongo import IndexModel
from sbos.minimal.models.domain import Domain
from sbos.minimal.models.user import User

from sbos.playground.config.manager import settings
from sbos.playground.models.app import App
from sbos.playground.models.permission import PermissionProfile

# class Domain(DomainBase):
#     users: list[BackLink["DomainUser"]] = Field(original_field="domain")
#     apps: list[BackLink["DomainApp"]] = Field(original_field="domain")
#     policies: list[BackLink["DomainPreActuationPolicy"]] = Field(
#         original_field="domain"
#     )


class DomainApp(Document):
    domain: Link[Domain]
    app: Link[App]
    # users: list[BackLink["DomainUserApp"]] = Field(original_field="domain_app")

    class Settings:
        name = "domain.apps"
        indexes = [
            IndexModel(["domain", "app"], unique=True),
        ]


class DomainUser(Document):
    domain: Link[Domain]
    user: Link[User]
    is_admin: bool = False
    # apps: list[BackLink["DomainUserApp"]] = Field(original_field="domain_user")
    # profiles: list[BackLink["DomainUserProfile"]] = Field(original_field="domain_user")

    class Settings:
        name = "domain.users"
        indexes = [
            IndexModel(["domain", "user"], unique=True),
        ]


class DomainUserApp(Document):
    domain: Link[Domain]
    user: Link[User]
    app: Link[App]
    # domain_user: Link[DomainUser]
    # domain_app: Link[DomainApp]
    status: str = ""
    container_id: str = ""
    arguments: dict[str, str] = {}
    token: str = ""

    if TYPE_CHECKING:
        domain: Link[Domain] | Domain
        user: Link[User] | User
        app: Link[App] | App
        domain_user: Link[DomainUser] | DomainUser
        domain_app: Link[DomainApp] | DomainApp

    class Settings:
        name = "domain.user.apps"
        indexes = [
            IndexModel(["domain", "user", "app"], unique=True),
            IndexModel(["domain", "user"]),
            IndexModel(["domain", "app"]),
        ]

    def get_container_name(self):
        return f"{settings.DOCKER_PREFIX}-{self.app.name}-{self.user.name}-{self.id}".replace(
            "@", "at"
        )


class DomainUserProfile(Document):
    domain: Link[Domain]
    user: Link[User]
    # domain_user: Link[DomainUser]
    profile: Link[PermissionProfile]
    arguments: dict

    class Settings:
        name = "domain.user.profiles"
        indexes = [
            IndexModel(["domain", "user"]),
        ]

    if TYPE_CHECKING:
        domain: Link[Domain] | Domain
        user: Link[User] | User
        profile: Link[PermissionProfile] | PermissionProfile


class DomainPreActuationPolicy(Document):
    domain: Link[Domain]
    name: str
    query: str = ""
    priority: int = 0
    guards: list[str]

    class Settings:
        name = "domain.policies"
        indexes = [
            IndexModel(["domain", "name"]),
        ]


class DomainResourceConstraint(Document):
    domain: Link[Domain]
    entity_id: str
    value: float

    class Settings:
        name = "domain.resources"
        indexes = [
            IndexModel(["domain", "entity_id"]),
        ]
