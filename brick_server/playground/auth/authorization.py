import json
from typing import Any, Callable, Dict, List, Optional, Set

from brick_server.minimal.auth.jwt import jwt_security_scheme, parse_jwt_token
from brick_server.minimal.dependencies import get_graphdb
from brick_server.minimal.exceptions import GraphDBError, InternalServerError
from brick_server.minimal.interfaces.cache import use_cache
from brick_server.minimal.models import Domain, get_doc, get_doc_or_none, get_docs
from brick_server.minimal.schemas import PermissionScope, PermissionType
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials
from loguru import logger

from brick_server.playground.models import (  # DefaultRole,; DomainRole,
    App,
    DomainApp,
    DomainOccupancy,
    DomainUser,
    DomainUserApp,
    DomainUserProfile,
    Entity,
    PermissionProfile,
    User,
)
from brick_server.playground.schemas import PermissionModel
from brick_server.playground.utils import parse_graphdb_result

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


def get_jwt_payload(
    token: HTTPAuthorizationCredentials = jwt_security_scheme,
) -> Dict[str, Any]:
    return parse_jwt_token(token.credentials)


def get_user_from_jwt(jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)) -> User:
    return get_doc(User, user_id=jwt_payload["user_id"])


def get_app_from_jwt(
    jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)
) -> Optional[App]:
    return get_doc_or_none(App, name=jwt_payload["app_name"])


def get_domain(domain: str = Path(..., description="Name of the domain")) -> Domain:
    # return ObjectId(domain)
    return get_doc_or_none(Domain, name=domain)


def get_app(app: str = Path(..., description="Name of the app")) -> App:
    return get_doc(App, name=app)


def get_user(user: str = Path(..., description="User Id of the user")) -> User:
    return get_doc(User, user_id=user)


def get_domain_user(
    user: User = Depends(get_user_from_jwt), domain: Domain = Depends(get_domain)
) -> Optional[DomainUser]:
    return get_doc_or_none(DomainUser, user=user.id, domain=domain.id)


def get_domain_app(
    domain: Domain = Depends(get_domain),
    app: App = Depends(get_app),
) -> DomainApp:
    return get_doc(DomainApp, domain=domain.id, app=app.id)


def get_domain_user_app(
    domain: Domain = Depends(get_domain),
    user: User = Depends(get_user_from_jwt),
    app: App = Depends(get_app),
) -> DomainUserApp:
    return get_doc(DomainUserApp, domain=domain.id, user=user.id, app=app.id)


def get_permission_profile(
    profile: str = Path(..., description="UUID of the permission profile"),
) -> DomainApp:
    return get_doc(PermissionProfile, id=profile)


# def get_domain_role(
#     domain_id: ObjectId = Depends(get_domain_id),
#     role_name: str = "basic",
# ) -> Optional[DomainRole]:
#     return get_doc_or_none(DomainRole, domain=domain_id, role_name=role_name)
#


def get_domain_occupancies(
    user: User = Depends(get_user_from_jwt), domain: Domain = Depends(get_domain)
) -> List[DomainOccupancy]:
    return get_docs(DomainOccupancy, user=user.id, domain=domain.id)


def get_domain_user_profiles(
    user: User = Depends(get_user_from_jwt), domain: Domain = Depends(get_domain)
) -> List[DomainUserProfile]:
    return get_docs(DomainUserProfile, user=user.id, domain=domain.id)


async def get_entity_obj(entity_id: str):
    entity_cls = ""
    return Entity(id=entity_id, cls=entity_cls)


class Authorization:
    def __init__(
        self,
        user: User,
        app: Optional[App] = None,
        domain: Optional[Domain] = None,
    ) -> None:
        self.user: User = user
        self.app: Optional[App] = app
        self.domain: Optional[Domain] = domain
        if self.domain is not None:
            self.domain_user: Optional[DomainUser] = get_domain_user(
                self.user, self.domain
            )
        else:
            self.domain_user: Optional[DomainUser] = None
        if self.domain is not None and self.app is not None:
            self.domain_user_app: Optional[DomainUserApp] = get_domain_user_app(
                self.domain, self.user, self.app
            )
        else:
            self.domain_user_app: Optional[DomainUserApp] = None
        # self.domain_user_app = ...
        # self.domain_occupancies = ...
        # self.domain_user = ...
        # self.domain_roles = {}
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

    async def query_entity_ids(self, query) -> List[str]:
        try:
            res = await self.brick_db.query(self.domain.name, query)
            parsed_res = parse_graphdb_result(res)
            assert len(parsed_res.keys()) == 1
            entity_ids = parsed_res[list(parsed_res.keys())[0]]
            return entity_ids
        except GraphDBError as e:
            logger.warning(repr(e))
            raise InternalServerError(hint="sparql")

    async def filter_entities_by_types(
        self, entity_ids: Set[str], types: List[str]
    ) -> Set[str]:
        entity_ids_string = ",".join(map(lambda x: f"<{x}>", entity_ids))
        type_query_string = "UNION".join(map(lambda x: f"{{?entity a {x}.}}", types))
        query = f"""
select distinct ?entity where {{
    {type_query_string}
    filter (?entity in ({entity_ids_string})).
}}
        """
        logger.info(query)
        return set(await self.query_entity_ids(query))

    async def get_authorized_entities_in_profile(
        self, profile, arguments, permission: PermissionType
    ) -> List[str]:
        async def fallback_func():
            template: str = profile.__getattribute__(permission)
            query = template.format(**arguments)
            # logger.info("{} {} {}", template, arguments, query)
            return await self.query_entity_ids(query)

        cache_key = f"permission_profile:{self.domain.name}:{profile.id}:{permission}:{json.dumps(arguments)}"
        # start = time.time()
        result = await use_cache(cache_key, fallback_func)
        # end = time.time()
        # logger.info("{} {}", profile.id, (end - start) * 1000)
        return result

    async def get_all_authorized_entities(self, permission: PermissionType) -> Set[str]:
        async def fallback_func():
            entity_ids = set()
            domain_user_profiles = get_domain_user_profiles(self.user, self.domain)
            for profile in domain_user_profiles:
                entity_ids_domain_user = await self.get_authorized_entities_in_profile(
                    profile.profile, profile.arguments, permission
                )
                entity_ids.update(entity_ids_domain_user)
            if self.domain_user_app is not None:
                entity_ids_app = await self.get_authorized_entities_in_profile(
                    self.app.profile, self.domain_user_app.arguments, permission
                )
                if self.app.permission_model == PermissionModel.AUGMENTATION:
                    entity_ids.update(entity_ids_app)
                elif self.app.permission_model == PermissionModel.INTERSECTION:
                    entity_ids.intersection_update(entity_ids_app)
            return entity_ids

        # only support one app instance in one domain per user
        cache_key = f"authorized_entities:{self.domain.name}:{self.app.name}:{self.user.user_id}"
        result = await use_cache(cache_key, fallback_func)
        return result

    async def check_profile(
        self,
        profile,
        arguments,
        entity_id: str,
        permission: PermissionType,
    ):
        entity_ids = await self.get_authorized_entities_in_profile(
            profile, arguments, permission
        )
        return entity_id in entity_ids

    async def check_entities_permission(
        self, entity_ids: Set[str], permission: PermissionType
    ) -> bool:
        # if the user is site admin, grant all permissions
        if self.user.is_admin:
            return True

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

        # entities must be in domain
        if self.domain is None:
            return False
        # user must exist in domain
        if self.domain_user is None:
            return False
        # if the user is domain admin, grant all permissions
        if self.domain_user.is_admin:
            return True

        if len(entity_ids) == 0:
            return False
        # TODO: entity_id -> entity_ids
        entity_id = entity_ids.pop()
        # entity = await get_entity_obj(entity_id)

        # # check permission by domain user roles
        # if await self.check_in_locations_by_role_names(
        #     self.domain_user.roles.items(), entity, permission
        # ):
        #     return True

        # check permission by domain_user_app profile
        if self.app is not None:
            # app must be installed by user
            if self.domain_user_app is None:
                return False
            authed = await self.check_profile(
                self.app.profile, self.domain_user_app.arguments, entity_id, permission
            )
            if self.app.permission_model == PermissionModel.AUGMENTATION and authed:
                return True
            if self.app.permission_model == PermissionModel.INTERSECTION and not authed:
                return False

        # check permission by domain_user profile
        domain_user_profiles = get_domain_user_profiles(self.user, self.domain)
        for profile in domain_user_profiles:
            if await self.check_profile(
                profile.profile, profile.arguments, entity_id, permission
            ):
                return True

        return False

    def check_admin_site(self) -> bool:
        return self.user.is_admin

    def check_admin_domain(self) -> bool:
        if self.check_admin_site():
            return True
        if self.domain_user is ...:
            self.domain_user = get_domain_user(self.user, self.domain)
        if self.domain_user is None:
            return False
        return self.domain_user.is_admin

    async def __call__(
        self,
        entity_ids: Set[str],
        permission_type: PermissionType,
        permission_scope: PermissionScope,
    ) -> bool:
        # app can only use read / write permission (on entities)
        if permission_scope == PermissionScope.SITE:
            return self.app is None and self.check_admin_site()
        elif permission_scope == PermissionScope.DOMAIN:
            return self.app is None and self.check_admin_domain()
        elif permission_scope == PermissionScope.USER:
            return self.app is None
        elif permission_scope == PermissionScope.ENTITY:
            if len(entity_ids) == 0:
                return True
            else:
                return await self.check_entities_permission(entity_ids, permission_type)
        return False

        # if self.app is not None and permission_type not in (PermissionType.READ, PermissionType.WRITE):
        #     return False
        # if permission_type == PermissionType.ADMIN_SITE:
        #     result = self.check_admin_site()
        # elif permission_type == PermissionType.ADMIN_DOMAIN:
        #     result = self.check_admin_domain()
        # elif len(entity_ids) == 0:
        #     result = True
        # else:
        #     result = await self.check_entities_permission(entity_ids, permission_type)
        # return result


def auth_logic(
    user: User = Depends(get_user_from_jwt),
    app: Optional[App] = Depends(get_app_from_jwt),
    domain: Optional[Domain] = Depends(get_domain),
) -> Callable[[Set[str], PermissionType, PermissionScope], bool]:
    authorization = Authorization(user, app, domain)

    # async def _auth_logic(entity_ids: Set[str], permission_type: PermissionType,
    #                       permission_scope: PermissionScope) -> bool:
    #     return await authorization(entity_ids, permission_type, permission_scope)

    return authorization


class DomainAdminPermissionChecker:
    def __call__(self, domain: str = Depends(get_domain)):
        # find a doc in DomainUser
        pass
