from enum import Enum

from brick_server.minimal.models import Domain, User
from mongoengine import (
    BooleanField,
    DictField,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)
from pydantic import BaseModel

from brick_server.playground.schemas import PermissionModel


class PermissionProfile(Document):
    read = StringField(required=True)
    write = StringField(required=True)


class App(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    profile = ReferenceField(PermissionProfile, required=True)
    approved = BooleanField(required=True, default=False)
    permission_model = StringField(required=True, default=PermissionModel.INTERSECTION)


class DomainApp(Document):
    domain = ReferenceField(Domain, required=True)
    app = ReferenceField(App, required=True)

    meta = {
        "indexes": [
            {
                "fields": ["domain", "app"],
                "unique": True,
            }
        ]
    }


class DomainUserApp(Document):
    domain = ReferenceField(Domain, required=True)
    user = ReferenceField(User, required=True)
    app = ReferenceField(App, required=True)
    status = StringField(default="")
    container_id = StringField(default="")
    arguments = DictField()

    meta = {
        "indexes": [
            {
                "fields": ["domain", "user", "app"],
                "unique": True,
            },
            {
                "fields": ["domain", "user"],
            },
        ]
    }

    def get_container_name(self):
        from brick_server.playground.config.manager import settings

        return f"{settings.DOCKER_PREFIX}-{self.app.name}-{self.user.user_id}-{self.id}".replace(
            "@", "at"
        )


class MarketApp(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    permission_templates = DictField(DictField())
    token_lifetime = IntField(default=3600)


class StagedApp(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    app_id = StringField(required=True, unique=True)
    permission_templates = DictField(DictField())
    """
    Example:
    {
        "znt_query": {
            "query": "select ?znt where {?znt ?p ?o.};",
            "permission_type": "R",
        }
    }
    """
    result_storages = DictField(
        DictField(StringField()),
        default={},
    )

    # valid = BooleanField(required=True)
    # expiration_date = DateTimeField(required=True)
    pending_approvals = ListField(StringField(help_text="Admin ID"))
    # rejected_approvals = DictField(ListField()) # pending approvals from users. If approved, the itme goes to approvals
    # approvals = DictField(ListField())
    # In both of the above cases, key is query name and list of the values are the owner IDs.
    installer = StringField()
    # admin = StringField() # user_id
    callback_url = StringField()
    token_lifetime = IntField(default=3600)
    app_expires_at = IntField()
    permission_lifetime = IntField(default=36000)


# class User(BrickUser):
#     activated_apps = ListField(ReferenceField(StagedApp), default=[])
#     meta = {
#         'collection': 'user'
#     }

# class PointType(str, Enum):
#     HVAC = "HVAC"
#     Temperature = "Temperature"


class Entity(BaseModel):
    id: str
    cls: str


# class Domain(Document):
#     name = StringField()


# class DomainRole(Document):
#     domain = ReferenceField(Domain, required=True)
#     role_name = StringField(required=True)
#     permissions = DictField(
#         StringField(),
#         help_text="EntityCls -> PermissionType",
#         default={},
#     )
#
#     meta = {
#         "indexes": [
#             {
#                 "fields": ["domain", "role_name"],
#                 "unique": True,
#             }
#         ]
#     }


class DomainUser(Document):
    domain = ReferenceField(Domain, required=True)
    user = ReferenceField(User, required=True)
    # roles = DictField(
    #     ReferenceField(DomainRole),
    #     help_text="brick location -> DomainRole",
    #     default={},
    # )
    # rooms = ListField(StringField())
    is_admin = BooleanField(default=False)

    meta = {
        "indexes": [
            {
                "fields": ["domain", "user"],
                "unique": True,
            }
        ]
    }


class DomainOccupancy(Document):
    domain = ReferenceField(Domain, required=True)
    user = ReferenceField(User, required=True)
    location: StringField(required=True)

    meta = {
        "indexes": [
            {
                "fields": ["domain", "user"],
                "unique": False,
            }
        ]
    }


class DomainUserProfile(Document):
    domain = ReferenceField(Domain, required=True)
    user = ReferenceField(User, required=True)
    profile = ReferenceField(PermissionProfile, required=True)
    arguments = DictField()

    meta = {
        "indexes": [
            {
                "fields": ["domain", "user"],
                "unique": False,
            }
        ]
    }


class DomainPreActuationPolicy(Document):
    domain = ReferenceField(Domain, required=True)
    name = StringField(required=True)
    query = StringField(required=True, default="")
    priority = IntField(required=True, default=0)
    guards = ListField(StringField())

    meta = {
        "indexes": [
            {
                "fields": ["domain", "name"],
                "unique": True,
            }
        ]
    }


# class AppProfile(Document):
#     app = ReferenceField(App, required=True)
#     profile = ReferenceField(PermissionProfile, required=True)
#     # TODO: add arguments in app instance
#     # arguments = DictField()


class StrEnumMixin(str, Enum):
    def __str__(self) -> str:
        return self.value


# class DefaultRole(StrEnumMixin, Enum):
#     BASIC = "basic"
#     ADMIN = "admin"
#
#
