import json
from typing import Callable

from brick_server.minimal.interfaces.cache import use_cache
from brick_server.minimal.securities.auth import (
    get_jwt_payload,
    get_token_user,
    my_jwt_strategy,
)
from fastapi import Depends
from fastapi_users.jwt import generate_jwt
from loguru import logger

from brick_server.playground.models import (
    App,
    Domain,
    DomainApp,
    DomainUser,
    DomainUserApp,
    User,
)
from brick_server.playground.schemas import (
    PermissionModel,
    PermissionScope,
    PermissionType,
)
from brick_server.playground.utilities.dependencies import (
    get_domain_user_profiles,
    get_graphdb,
    get_path_domain,
    get_path_domain_optional,
)
from brick_server.playground.utilities.exceptions import BizError, ErrorCode


async def get_token_domain(
    token: dict | None = Depends(get_jwt_payload),
) -> Domain | None:
    try:
        domain_name = token.get("domain")
        domain = await Domain.find_one(Domain.name == domain_name)
        return domain
    except Exception:
        return None


async def get_token_app(
    token: dict | None = Depends(get_jwt_payload),
) -> App | None:
    try:
        app_name = token.get("app")
        app = await App.find_one(App.name == app_name)
        return app
    except Exception:
        return None


async def get_domain_user(
    domain: Domain = Depends(get_path_domain),
    user: User = Depends(get_token_user),
) -> DomainUser | None:
    return await DomainUser.find_one(
        DomainUser.domain.id == domain.id, DomainUser.user.id == user.id
    )


async def get_domain_app(
    domain: Domain = Depends(get_path_domain),
    app: App = Depends(get_token_app),
) -> DomainApp:
    domain_app = await DomainApp.find_one(
        DomainApp.domain.id == domain.id, DomainApp.app.id == app.id
    )
    if domain_app is None:
        raise BizError(ErrorCode.DomainAppNotFoundError)
    return domain_app


async def get_domain_user_app(
    domain: Domain = Depends(get_path_domain),
    user: User = Depends(get_token_user),
    app: App = Depends(get_token_app),
) -> DomainUserApp:
    domain_user_app = await DomainUserApp.find_one(
        DomainUserApp.domain.id == domain.id,
        DomainUserApp.user.id == user.id,
        DomainUserApp.app.id == app.id,
    )
    if domain_user_app is None:
        raise BizError(ErrorCode.DomainUserAppNotFoundError)
    return domain_user_app


class Authorization:
    def __init__(
        self,
        user: User,
        app: App | None = None,
        domain: Domain | None = None,
    ) -> None:
        self.user = user
        self.app = app
        self.domain = domain
        self.domain_user: DomainUser | None = None
        self.domain_user_app: DomainUserApp | None = None
        self.brick_db = get_graphdb()

    def __await__(self):
        return self.async_init().__await__()

    async def async_init(self) -> "Authorization":
        if self.domain is not None:
            self.domain_user = await get_domain_user(self.domain, self.user)
        if self.domain is not None and self.app is not None:
            self.domain_user_app = await get_domain_user_app(
                self.domain, self.user, self.app
            )
        return self

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

    async def query_entity_ids(self, query) -> tuple[list[str], dict[str, str]]:
        try:
            result, prefixes = await self.brick_db.query(self.domain.name, query)
            parsed_res = self.brick_db.parse_result(result, prefixes)
            assert len(parsed_res.keys()) == 1
            entity_ids = parsed_res[list(parsed_res.keys())[0]]
            return entity_ids, prefixes
        except BizError as e:
            logger.warning(repr(e))
            raise e

    async def query_entity_types(self, query, prefixes) -> dict[str, set[str]]:
        try:
            result, new_prefixes = await self.brick_db.query(self.domain.name, query)
            new_prefixes.update(prefixes)
            parsed_res = self.brick_db.parse_result(result, new_prefixes)
            logger.info(parsed_res)
            assert len(parsed_res.keys()) == 2
            entity_ids = parsed_res[list(parsed_res.keys())[0]]
            entity_types = parsed_res[list(parsed_res.keys())[1]]
            result = {}
            for entity_id, entity_type in zip(entity_ids, entity_types):
                if entity_type not in result:
                    result[entity_type] = {entity_id}
                else:
                    result[entity_type].add(entity_id)
            return result
        except BizError as e:
            logger.warning(repr(e))
            raise e

    async def filter_entities_by_types(
        self, entity_ids: set[str], types: list[str], prefixes: dict[str, str]
    ) -> dict[str, set[str]]:
        # entity_ids_string = ",".join(map(lambda x: f"<{x}>", entity_ids))
        entity_ids_string = ",".join(entity_ids)
        type_query_string = ",".join(types)

        query = f"""
select distinct ?entity ?type where {{
    ?entity a ?type
    filter (?entity in ({entity_ids_string})).
    filter (?type in ({type_query_string}))
}}
        """

        # type_query_string = "UNION".join(map(lambda x: f"{{?entity a {x}.}}", types))
        #         query = f"""
        # select distinct ?entity where {{
        #     {type_query_string}
        #     filter (?entity in ({entity_ids_string})).
        # }}
        #         """
        logger.info(query)
        result = await self.query_entity_types(query, prefixes)
        logger.info(result)
        return result
        # return set()
        # return set(await self.query_entity_ids(query))

    @staticmethod
    def intersect_types_dict(
        original_entity_ids: set[str], types_dict: dict[str, set[str]]
    ) -> dict[str, list[str]]:
        result = {}
        for entity_type, entity_ids in types_dict.items():
            _entity_ids = list(entity_ids.intersection(original_entity_ids))
            if len(_entity_ids) > 0:
                result[entity_type] = _entity_ids
        return result

    async def get_authorized_entities_in_profile(
        self, profile, arguments, permission: PermissionType
    ) -> tuple[list[str], dict[str, str]]:
        async def fallback_func() -> tuple[list[str], dict[str, str]]:
            template: str = profile.__getattribute__(permission)
            query = template.format(**arguments)
            logger.info("{} {} {}", template, arguments, query)
            return await self.query_entity_ids(query)

        cache_key = f"{self.domain.name}:permission_profile:{profile.id}:{permission}:{json.dumps(arguments)}"
        # start = time.time()
        result = await use_cache(cache_key, fallback_func)
        logger.info("{}", result)
        # end = time.time()
        # logger.info("{} {}", profile.id, (end - start) * 1000)
        return result

    async def get_all_authorized_entities(
        self, permission: PermissionType
    ) -> tuple[set[str], dict[str, str]]:
        async def fallback_func() -> tuple[set[str], dict[str, str]]:
            entity_ids = set()
            prefixes = {}
            domain_user_profiles = await get_domain_user_profiles(
                self.domain, self.user
            )
            for profile in domain_user_profiles:
                entity_ids_domain_user, prefixes_domain_user = (
                    await self.get_authorized_entities_in_profile(
                        profile.profile, profile.arguments, permission
                    )
                )
                entity_ids.update(entity_ids_domain_user)
                prefixes.update(prefixes_domain_user)
            if self.domain_user_app is not None:
                entity_ids_app, prefixes_app = (
                    await self.get_authorized_entities_in_profile(
                        self.app.profile, self.domain_user_app.arguments, permission
                    )
                )
                if self.app.permission_model == PermissionModel.AUGMENTATION:
                    entity_ids.update(entity_ids_app)
                elif self.app.permission_model == PermissionModel.INTERSECTION:
                    entity_ids.intersection_update(entity_ids_app)
                prefixes.update(prefixes_app)
            return entity_ids, prefixes

        # only support one app instance in one domain per user
        if self.app is not None:
            app_name = self.app.name
        else:
            app_name = "_"
        cache_key = f"{self.domain.name}:authorized_entities:{app_name}:{self.user.name}:{permission}"
        result = await use_cache(cache_key, fallback_func)
        return result

    async def check_profile(
        self,
        profile,
        arguments,
        entity_id: str,
        permission: PermissionType,
    ):
        entity_ids, prefixes = await self.get_authorized_entities_in_profile(
            profile, arguments, permission
        )
        return entity_id in entity_ids

    async def check_entities_permission(
        self, entity_ids: set[str], permission: PermissionType
    ) -> bool:
        # if the user is site admin, grant all permissions
        if self.user.is_superuser:
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
        domain_user_profiles = await get_domain_user_profiles(self.domain, self.user)
        for profile in domain_user_profiles:
            if await self.check_profile(
                profile.profile, profile.arguments, entity_id, permission
            ):
                return True

        return False

    def check_admin_site(self) -> bool:
        return self.user.is_superuser

    async def check_admin_domain(self) -> bool:
        if self.check_admin_site():
            return True
        if self.domain_user is ...:
            self.domain_user = await get_domain_user(self.domain, self.user)
        if self.domain_user is None:
            return False
        return self.domain_user.is_admin

    async def __call__(
        self,
        entity_ids: set[str],
        permission_type: PermissionType,
        permission_scope: PermissionScope,
    ) -> bool:
        # app can only use read / write permission (on entities)
        if permission_scope == PermissionScope.SITE:
            return self.app is None and self.check_admin_site()
        elif permission_scope == PermissionScope.DOMAIN:
            return self.app is None and await self.check_admin_domain()
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


async def auth_logic(
    user: User = Depends(get_token_user),
    app: App | None = Depends(get_token_app),
    domain: Domain | None = Depends(get_path_domain_optional),
) -> Callable[[set[str], PermissionType, PermissionScope], bool]:
    authorization = await Authorization(user, app, domain)

    # async def _auth_logic(entity_ids: set[str], permission_type: PermissionType,
    #                       permission_scope: PermissionScope) -> bool:
    #     return await authorization(entity_ids, permission_type, permission_scope)

    return authorization


async def create_jwt_token(
    domain: Domain,
    user: User,
    app: App,
    domain_user_app: DomainUserApp | None = None,
    token_lifetime: int = my_jwt_strategy.lifetime_seconds,
):
    if domain_user_app is None and domain is not None and app is not None:
        domain_user_app = await get_domain_user_app(domain, user, app)

    data = {
        "sub": str(user.email),
        "aud": my_jwt_strategy.token_audience,
        "domain": domain.name if domain is not None else None,
        "app": app.name if app is not None else None,
        "domain_user_app": str(domain_user_app.id) if domain_user_app else None,
    }
    return generate_jwt(
        data,
        my_jwt_strategy.encode_key,
        token_lifetime,
        algorithm=my_jwt_strategy.algorithm,
    )
