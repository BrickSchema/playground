from typing import Any, Dict, List, Optional, Set

from brick_server.minimal.exceptions import DoesNotExistError
from bson import ObjectId
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials
from loguru import logger

from brick_server.minimal.auth.jwt import jwt_security_scheme, parse_jwt_token
from brick_server.minimal.models import get_doc, get_docs, Domain
from brick_server.minimal.dependencies import get_graphdb

from ..models import (
    # DefaultRole,
    DomainOccupancy,
    DomainUserProfile,
    # DomainRole,
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
    except DoesNotExistError:
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


def get_domain(
        domain: str = Path(..., description="Name of the domain")
) -> Domain:
    # return ObjectId(domain)
    return get_doc(Domain, name=domain)


def get_domain_user(
        user: User = Depends(get_current_user), domain: Domain = Depends(get_domain)
) -> Optional[DomainUser]:
    return get_doc_or_none(DomainUser, user=user.id, domain=domain.id)


# def get_domain_role(
#     domain_id: ObjectId = Depends(get_domain_id),
#     role_name: str = "basic",
# ) -> Optional[DomainRole]:
#     return get_doc_or_none(DomainRole, domain=domain_id, role_name=role_name)
#

def get_domain_occupancies(
        user: User = Depends(get_current_user), domain: Domain = Depends(get_domain)
) -> List[DomainOccupancy]:
    return get_docs(DomainOccupancy, user=user.id, domain=domain.id)


def get_domain_user_profiles(
        user: User = Depends(get_current_user), domain: Domain = Depends(get_domain)
) -> List[DomainUserProfile]:
    return get_docs(DomainUserProfile, user=user.id, domain=domain.id)


async def get_entity_obj(entity_id: str):
    entity_cls = ""
    return Entity(id=entity_id, cls=entity_cls)


class Authorization:
    def __init__(
            self,
            user: User = Depends(get_current_user),
            app: Optional[StagedApp] = Depends(get_staged_app),
            domain: Optional[Domain] = None,
    ) -> None:
        self.user = user
        self.app = app
        self.domain = domain
        self.domain_occupancies = ...
        self.domain_user = ...
        self.domain_roles = {}
        self.brick_db = get_graphdb()

    # def check_entity_permission(
    #     self,
    #     entity: Entity,
    #     permission: PermissionType,
    #     domain_role: DomainRole,
    # ) -> bool:
    #     if self.app is not None:
    #         # self.app.
    #         # app mask
    #         ...
    #     db_permission = domain_role.permissions.get(entity.cls, None)
    #     if db_permission == str(PermissionType.WRITE):
    #         return True
    #     if (
    #         db_permission == str(PermissionType.READ)
    #         and permission == PermissionType.READ
    #     ):
    #         return True
    #     return False
    #
    # async def is_entity_in_location(self, location: str, entity: Entity) -> bool:
    #     query = ""
    #     raw_res = await self.brick_db.query(query)
    #     return True
    #
    # async def check_in_locations_by_role_names(
    #     self, zipped, entity: Entity, permission: PermissionType
    # ) -> bool:
    #     for location, role_name in zipped:
    #         if await self.is_entity_in_location(location, entity):
    #             if (self.domain_id, role_name) not in self.domain_roles:
    #                 self.domain_roles[(self.domain_id, role_name)] = get_domain_role(
    #                     self.domain_id, role_name
    #                 )
    #             domain_role = self.domain_roles[(self.domain_id, role_name)]
    #             if domain_role is None:
    #                 continue
    #             if self.check_entity_permission(
    #                 entity=entity,
    #                 permission=permission,
    #                 domain_role=domain_role,
    #             ):
    #                 return True
    #     return False

    async def check_profile(
            self,
            profile,
            entity: Entity,
            permission: PermissionType,
    ):

        template: str = profile.profile.__getattribute__(permission)
        query = template.format(**profile.arguments)
        logger.info("{} {} {}", template, profile.arguments, query)

        # TODO: cache in redis
        raw_res = await self.brick_db.query(self.domain.name, query)


        return False

    async def check(self, entity_ids: Set[str], permission: PermissionType) -> bool:
        # TODO: entity_id -> entity_ids
        entity_id = entity_ids.pop()
        # if the user is site admin, grant all permissions
        if self.user.is_admin:
            return True
        entity = await get_entity_obj(entity_id)

        # # check permission in domain occupancy list
        # if self.domain_occupancies is ...:
        #     self.domain_occupancies = get_domain_occupancies(self.user, self.domain_id)
        #
        # locations = [
        #     domain_occupancy.location for domain_occupancy in self.domain_occupancies
        # ]
        # role_names = [str(DefaultRole.BASIC)] * len(locations)
        # if await self.check_in_locations_by_role_names(
        #     zip(locations, role_names), entity, permission
        # ):
        #     return True

        # get domain user info
        if self.domain_user is ...:
            self.domain_user = get_domain_user(self.user, self.domain)
        if self.domain_user is None:
            return False
        if self.domain_user.is_admin:
            return True

        # # check permission by domain user roles
        # if await self.check_in_locations_by_role_names(
        #     self.domain_user.roles.items(), entity, permission
        # ):
        #     return True

        # check permission by domain user profile
        domain_user_profiles = get_domain_user_profiles(self.user, self.domain)
        for profile in domain_user_profiles:
            if await self.check_profile(profile, entity, permission):
                return True

        return False

    async def __call__(self, entity_ids: Set[str], permission: PermissionType) -> bool:
        if not await self.check(entity_ids, permission):
            raise Exception("Permission denied")
        return True


def auth_logic(
        user: User = Depends(get_current_user),
        app: Optional[StagedApp] = Depends(get_staged_app),
        domain: Optional[Domain] = Depends(get_domain),
) -> Authorization:
    authorization = Authorization(user, app, domain)
    async def _auth_logic(entity_ids: Set[str], permission: PermissionType):
        return await authorization(entity_ids, permission)

    return _auth_logic


class DomainAdminPermissionChecker:
    def __call__(self, domain: str = Depends(get_domain)):
        # find a doc in DomainUser
        pass
