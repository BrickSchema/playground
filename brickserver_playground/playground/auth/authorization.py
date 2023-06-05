from typing import Any, Dict, List, Optional

from brick_server.auth.authorization import parse_jwt_token
from brick_server.dbs import BrickSparqlAsync
from brick_server.dependencies import get_brick_db
from brick_server.models import get_doc, get_docs
from brick_server.services.models import jwt_security_scheme
from bson import ObjectId
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials

from ..models import (
    DefaultRole,
    DomainOccupancy,
    DomainRole,
    DomainUser,
    Entity,
    PermissionType,
    StagedApp,
    User,
)

SEP = "^#$%"


# def make_permission_key(user_id, app_name, entity_id):
#     return user_id + SEP + app_name + SEP + entity_id
#
#
# def check_permissions(entity_ids, user, app, permission_required):
#     for entity_id in entity_ids:
#         perm_key = make_permission_key(user.user_id, app.name, entity_id)
#         perm = r.get(perm_key)
#         if perm is None:
#             raise exceptions.Unauthorized(
#                 "The token does not have any permission over {0}".format(entity_id)
#             )
#         perm = perm.decode("utf-8")
#         perm_type, perm_start_time, perm_end_time = decode_permission_val(perm)
#         if permission_required not in perm_type:
#             raise exceptions.Unauthorized(
#                 "The token does not have `{0}` permission for {1}".format(
#                     permission_required, entity_id
#                 )
#             )
#         curr_time = time.time()
#         if curr_time < perm_start_time or curr_time > perm_end_time:
#             raise exceptions.Unauthorized("The token is not valid at the current time.")
#     return True
#
#
# def evaluate_app_user(action_type, target_ids, *args, **kwargs):
#     jwt_payload = parse_jwt_token(kwargs["token"].credentials)
#     app = get_doc(StagedApp, name=jwt_payload["app_id"])
#     user = get_doc(User, user_id=jwt_payload["user_id"])
#     check_permissions(target_ids, user, app, action_type)


def get_doc_or_none(doc_type: Any, **query):
    try:
        return get_doc(doc_type, **query)
    except doc_type.DoesNotExist:
        return None


def get_jwt_payload(
    token: HTTPAuthorizationCredentials = jwt_security_scheme,
) -> Dict[str, Any]:
    return parse_jwt_token(token.credentials)


def get_current_user(jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)) -> User:
    return get_doc(User, user_id=jwt_payload["user_id"])


def get_staged_app(
    jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)
) -> Optional[StagedApp]:
    return get_doc_or_none(StagedApp, name=jwt_payload["app_id"])


def get_domain_id(
    domain: str = Path(..., description="ObjectId of the domain")
) -> ObjectId:
    return ObjectId(domain)
    # return get_doc(Domain, _id=domain)


def get_domain_user(
    user: User = Depends(get_current_user), domain_id: ObjectId = Depends(get_domain_id)
) -> Optional[DomainUser]:
    return get_doc_or_none(DomainUser, user=user.id, domain=domain_id)


def get_domain_role(
    domain_id: ObjectId = Depends(get_domain_id),
    role_name: str = "basic",
) -> Optional[DomainRole]:
    return get_doc_or_none(DomainRole, domain=domain_id, role_name=role_name)


def get_domain_occupancies(
    user: User = Depends(get_current_user), domain_id: ObjectId = Depends(get_domain_id)
) -> List[DomainOccupancy]:
    return get_docs(DomainOccupancy, user=user.id, domain=domain_id)


async def get_entity_obj(brick_db: BrickSparqlAsync, entity_id: str):
    entity_cls = ""
    return Entity(id=entity_id, cls=entity_cls)


class Authorization:
    def __init__(
        self,
        brick_db: BrickSparqlAsync = Depends(get_brick_db),
        user: User = Depends(get_current_user),
        app: Optional[StagedApp] = Depends(get_staged_app),
        domain_id: Optional[ObjectId] = None,
    ) -> None:
        self.brick_db = brick_db

        self.user = user
        self.app = app
        self.domain_id = domain_id
        self.domain_occupancies = ...
        self.domain_user = ...
        self.domain_roles = {}

    def check_entity_permission(
        self,
        entity: Entity,
        permission: PermissionType,
        domain_role: DomainRole,
    ) -> bool:
        if self.app is not None:
            # self.app.
            # app mask
            ...
        db_permission = domain_role.permissions.get(entity.cls, None)
        if db_permission == str(PermissionType.WRITE):
            return True
        if (
            db_permission == str(PermissionType.READ)
            and permission == PermissionType.READ
        ):
            return True
        return False

    async def is_entity_in_location(self, location: str, entity: Entity) -> bool:
        query = ""
        raw_res = await self.brick_db.query(query)
        return True

    def check_in_locations_by_role_names(
        self, zipped, entity: Entity, permission: PermissionType
    ) -> bool:
        for location, role_name in zipped:
            if await self.is_entity_in_location(location, entity):
                if (self.domain_id, role_name) not in self.domain_roles:
                    self.domain_roles[(self.domain_id, role_name)] = get_domain_role(
                        self.domain_id, role_name
                    )
                domain_role = self.domain_roles[(self.domain_id, role_name)]
                if domain_role is None:
                    continue
                if self.check_entity_permission(
                    entity=entity,
                    permission=permission,
                    domain_role=domain_role,
                ):
                    return True
        return False

    def check(self, entity_id: str, permission: PermissionType) -> bool:
        # if the user is site admin, grant all permissions
        if self.user.is_admin:
            return True
        entity = await get_entity_obj(self.brick_db, entity_id)

        # check permission in domain occupancy list
        if self.domain_occupancies is ...:
            self.domain_occupancies = get_domain_occupancies(self.user, self.domain_id)

        locations = [
            domain_occupancy.location for domain_occupancy in self.domain_occupancies
        ]
        role_names = [str(DefaultRole.BASIC)] * len(locations)
        if self.check_in_locations_by_role_names(
            zip(locations, role_names), entity, permission
        ):
            return True

        # get domain user info
        if self.domain_user is ...:
            self.domain_user = get_domain_user(self.user, self.domain_id)
        if self.domain_user is None:
            return False
        if self.domain_user.is_superuser:
            return True

        # check permission by domain user roles
        if self.check_in_locations_by_role_names(
            self.domain_user.roles.items(), entity, permission
        ):
            return True

        return False

    def __call__(self, entity_id: str, permission: PermissionType):
        if not self.check(entity_id, permission):
            raise Exception("Permission denied")


def auth_logic(
    brick_db: BrickSparqlAsync = Depends(get_brick_db),
    user: User = Depends(get_current_user),
    app: Optional[StagedApp] = Depends(get_staged_app),
    domain_id: Optional[ObjectId] = None,
) -> Authorization:
    return Authorization(brick_db, user, app, domain_id)
