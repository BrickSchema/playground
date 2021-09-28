from enum import Enum

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

from brick_server.minimal.models import User as BrickUser


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


class User(BrickUser):
    activated_apps = ListField(ReferenceField(StagedApp), default=[])


# class PointType(str, Enum):
#     HVAC = "HVAC"
#     Temperature = "Temperature"


class Entity(BaseModel):
    id: str
    cls: str


class Domain(Document):
    name = StringField()


class DomainRole(Document):
    domain = ReferenceField(Domain, required=True)
    role_name = StringField(required=True)
    permissions = DictField(
        StringField(),
        help_text="EntityCls -> PermissionType",
        default={},
    )

    meta = {
        "indexes": [
            {
                "fields": ["domain", "role_name"],
                "unique": True,
            }
        ]
    }


class DomainUser(Document):
    domain = ReferenceField(Domain, required=True)
    user = ReferenceField(User, required=True)
    roles = DictField(
        ReferenceField(DomainRole),
        help_text="brick location -> DomainRole",
        default={},
    )
    # rooms = ListField(StringField())
    is_superuser = BooleanField(default=False)

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


class StrEnumMixin(str, Enum):
    def __str__(self) -> str:
        return self.value


class DefaultRole(StrEnumMixin, Enum):
    BASIC = "basic"
    ADMIN = "admin"


class PermissionType(StrEnumMixin, Enum):
    READ = "read"
    WRITE = "write"
