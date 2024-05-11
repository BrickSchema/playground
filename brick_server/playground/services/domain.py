from brick_server.minimal.interfaces.cache import clear_cache
from brick_server.minimal.securities.checker import PermissionChecker
from brick_server.minimal.services.domain import router
from fastapi import Body, Depends, Path
from fastapi_restful.cbv import cbv

from brick_server.playground import models, schemas
from brick_server.playground.interfaces import (
    ActuationInterface,
    AsyncpgTimeseries,
    SchedulingPolicyNaive,
)
from brick_server.playground.securities.auth import (  # get_app,; get_path_domain,; get_path_domain_user_profiles,; get_path_user,
    get_domain_user,
)
from brick_server.playground.utilities.dependencies import (
    get_actuation_iface,
    get_domain_user_profiles,
    get_path_app,
    get_path_domain,
    get_path_domain_policy,
    get_path_domain_user,
    get_path_profile,
    get_path_user,
    get_ts_db,
)
from brick_server.playground.utilities.exceptions import BizError, ErrorCode


@cbv(router)
class DomainAppRoute:
    @router.post(
        "/{domain}/apps/{app}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def domain_approve_app(
        self,
        domain: models.Domain = Depends(get_path_domain),
        app: models.App = Depends(get_path_app),
    ) -> schemas.StandardResponse[schemas.DomainAppRead]:
        if not app.approved:
            raise BizError(ErrorCode.AppNotApprovedError)
        domain_app = models.DomainApp(
            domain=domain.id,
            app=app.id,
        )
        try:
            await domain_app.save()
        except Exception as e:
            # TODO: catch the precise already exist exception
            raise BizError(ErrorCode.DomainAppAlreadyExistsError)
        domain_app.domain = domain
        domain_app.app = app
        return schemas.DomainAppRead.model_validate(domain_app.dict()).to_response()

    @router.get(
        "/{domain}/apps",
        dependencies=[Depends(PermissionChecker())],
    )
    async def domain_list_app(
        self,
        domain: models.Domain = Depends(get_path_domain),
    ) -> schemas.StandardListResponse[schemas.DomainAppRead]:
        domain_apps = await models.DomainApp.find_many(
            models.DomainApp.domain.id == domain.id,
            fetch_links=True,
            nesting_depth=1,
        ).to_list()
        return schemas.StandardListResponse(
            results=[
                schemas.DomainAppRead.model_validate(domain_app.dict())
                for domain_app in domain_apps
            ]
        )

    @router.get(
        "/{domain}/apps/{app}",
        dependencies=[Depends(PermissionChecker())],
    )
    async def domain_get_app(
        self,
        domain: models.Domain = Depends(get_path_domain),
        app: models.App = Depends(get_path_app),
    ) -> schemas.StandardResponse[schemas.DomainAppRead]:
        domain_app = await models.DomainApp.find_one(
            models.DomainApp.domain.id == domain.id,
            models.DomainApp.app.id == app.id,
        )
        if domain_app is None:
            raise BizError(ErrorCode.DomainAppNotFoundError)
        domain_app.domain = domain
        domain_app.app = app
        return schemas.DomainAppRead.model_validate(domain_app.dict()).to_response()


@cbv(router)
class DomainUserRoute:

    @router.post(
        "/{domain}/users/{user}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def add_domain_user(
        self,
        domain: models.Domain = Depends(get_path_domain),
        user: models.User = Depends(get_path_user),
    ) -> schemas.StandardResponse[schemas.DomainUserRead]:
        domain_user = models.DomainUser(domain=domain, user=user)
        try:
            await domain_user.save()

        except Exception:
            # TODO: catch the precise already exist exception
            raise BizError(ErrorCode.DomainUserAlreadyExistsError)
        domain_user.domain = domain
        domain_user.user = user
        return schemas.DomainUserRead.model_validate(domain_user.dict()).to_response()

    @router.get(
        "/{domain}/users/{user}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def get_domain_user(
        self,
        domain: models.Domain = Depends(get_path_domain),
        user: models.User = Depends(get_path_user),
    ) -> schemas.StandardResponse[schemas.DomainUserRead]:
        domain_user = await get_domain_user(domain, user)
        if domain_user is None:
            raise BizError(ErrorCode.DomainUserNotFoundError)
        domain_user.domain = domain
        domain_user.user = user
        return schemas.DomainUserRead.model_validate(domain_user.dict()).to_response()

    @router.get(
        "/{domain}/users",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def list_domain_user(
        self,
        domain: models.Domain = Depends(get_path_domain),
    ) -> schemas.StandardListResponse[schemas.DomainUserRead]:
        domain_users = await models.DomainUser.find_many(
            models.DomainUser.domain.id == domain.id,
            fetch_links=True,
            nesting_depth=1,
        ).to_list()
        return schemas.StandardListResponse(
            [
                schemas.DomainUserRead.model_validate(domain_user.dict())
                for domain_user in domain_users
            ]
        )


@cbv(router)
class DomainUserProfileRoute:
    domain: models.Domain = Depends(get_path_domain)
    user: models.User = Depends(get_path_user)
    domain_user: models.DomainUser = Depends(get_path_domain_user)

    @router.post(
        "/{domain}/users/{user}/profiles",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def add_domain_user_profile(
        self,
        domain_user_profile_create: schemas.DomainUserProfileCreate = Body(),
    ) -> schemas.StandardResponse[schemas.DomainUserProfileRead]:
        profile = await models.PermissionProfile.get(domain_user_profile_create.profile)
        if profile is None:
            raise BizError(ErrorCode.PermissionProfileNotFoundError)
        domain_user_profile = await models.DomainUserProfile.find_one(
            models.DomainUserProfile.domain.id == self.domain.id,
            models.DomainUserProfile.user.id == self.user.id,
            models.DomainUserProfile.profile.id == profile.id,
        )
        if domain_user_profile is not None:
            raise BizError(ErrorCode.PermissionProfileAlreadyExistsError)
        domain_user_profile = models.DomainUserProfile(
            domain=self.domain,
            user=self.user,
            profile=profile,
            arguments=domain_user_profile_create.arguments,
        )
        try:
            await domain_user_profile.save()
            await clear_cache(
                f"{self.domain.name}:authorized_entities:_:{self.user.name}"
            )
            return schemas.DomainUserProfileRead.model_validate(
                domain_user_profile.dict()
            ).to_response()
        except Exception as e:
            # should be unreachable
            raise BizError(ErrorCode.InternalServerError, str(e))

    @router.patch(
        "/{domain}/users/{user}/profiles/{profile}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def update_domain_user_profile(
        self,
        profile: models.PermissionProfile = Depends(get_path_profile),
        domain_user_profile_update: schemas.DomainUserProfileUpdate = Body(),
    ) -> schemas.StandardResponse[schemas.DomainUserProfileRead]:
        domain_user_profile = await models.DomainUserProfile.find_one(
            models.DomainUserProfile.domain.id == self.domain.id,
            models.DomainUserProfile.user.id == self.user.id,
            models.DomainUserProfile.profile.id == profile.id,
        )
        if domain_user_profile is None:
            raise BizError(ErrorCode.PermissionProfileNotFoundError)
        domain_user_profile.arguments = domain_user_profile_update.arguments
        try:
            await domain_user_profile.save()
            await clear_cache(
                f"{self.domain.name}:authorized_entities:_:{self.user.name}"
            )
            domain_user_profile.domain = self.domain
            domain_user_profile.user = self.user
            domain_user_profile.profile = profile
            return schemas.DomainUserProfileRead.model_validate(
                domain_user_profile.dict()
            ).to_response()
        except Exception as e:
            # should be unreachable
            raise BizError(ErrorCode.InternalServerError, str(e))

    @router.get(
        "/{domain}/users/{user}/profiles",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def list_domain_user_profile(
        self,
    ) -> schemas.StandardListResponse[schemas.DomainUserProfileRead]:
        domain_user_profiles = await get_domain_user_profiles(self.domain, self.user)
        return schemas.StandardListResponse(
            [
                schemas.DomainUserProfileRead.model_validate(profile.dict())
                for profile in domain_user_profiles
            ]
        )

    @router.delete(
        "/{domain}/users/{user}/profiles/{profile}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def delete_domain_user_profile(
        self,
        profile: models.PermissionProfile = Depends(get_path_profile),
    ) -> schemas.StandardResponse[schemas.Empty]:
        domain_user_profile = await models.DomainUserProfile.find_one(
            models.DomainUserProfile.domain.id == self.domain.id,
            models.DomainUserProfile.user.id == self.user.id,
            models.DomainUserProfile.profile.id == profile.id,
        )
        if domain_user_profile is None:
            raise BizError(ErrorCode.PermissionProfileNotFoundError)
        await domain_user_profile.delete()
        await clear_cache(f"{self.domain.name}:authorized_entities:_:{self.user.name}")
        return schemas.StandardResponse()

    # @router.get("/{domain}/user_profiles_arguments")
    # async def get_path_domain_user_profiles_arguments(
    #     self,
    #     profiles: List[models.DomainUserProfile] = Depends(
    #         get_path_domain_user_profiles
    #     ),
    #     checker: Authorization = Depends(
    #         PermissionChecker(permission_scope=PermissionScope.ENTITY)
    #     ),
    # ) -> List[Dict[str, str]]:
    #     return [profile.arguments for profile in profiles]


@cbv(router)
class DomainPreActuationPolicy:
    domain: models.Domain = Depends(get_path_domain)

    @router.get(
        "/{domain}/policies",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def list_domain_pre_actuation_policies(
        self,
    ) -> schemas.StandardListResponse[schemas.DomainPreActuationPolicyRead]:
        policies = await models.DomainPreActuationPolicy.find_many(
            models.DomainPreActuationPolicy.domain.id == self.domain.id
        ).to_list()
        return schemas.StandardListResponse(
            [
                schemas.DomainPreActuationPolicyRead.model_validate(
                    {
                        **policy.dict(),
                        "domain": self.domain.dict(),
                    }
                )
                for policy in policies
            ]
        )

    @router.post(
        "/{domain}/policies",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def create_domain_pre_actuation_policy(
        self,
        pre_actuation_policy_create: schemas.DomainPreActuationPolicyCreate = Body(...),
    ) -> schemas.StandardResponse[schemas.DomainPreActuationPolicyRead]:
        policy = models.DomainPreActuationPolicy(
            domain=self.domain,
            **pre_actuation_policy_create.dict(),
        )
        try:
            await policy.save()
        except Exception as e:
            # TODO: catch the precise already exist exception
            raise BizError(ErrorCode.DomainPreActuationPolicyAlreadyExistsError)
        await clear_cache(f"{self.domain.name}:policy")
        policy.domain = self.domain
        return schemas.DomainPreActuationPolicyRead.model_validate(
            policy.dict()
        ).to_response()

    @router.patch(
        "/{domain}/policies/{policy}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def update_domain_pre_actuation_policy(
        self,
        policy: models.DomainPreActuationPolicy = Depends(get_path_domain_policy),
        policy_update: schemas.DomainPreActuationPolicyUpdate = Body(),
    ) -> schemas.StandardResponse[schemas.DomainPreActuationPolicyRead]:
        policy_update.update_model(policy)
        await policy.save()
        await clear_cache(f"{self.domain.name}:policy")
        await clear_cache(f"{self.domain.name}:policy_query:{policy.id}")
        policy.domain = self.domain
        return schemas.DomainPreActuationPolicyRead.model_validate(
            policy.dict()
        ).to_response()

    @router.delete(
        "/{domain}/policies/{policy}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def delete_domain_pre_actuation_policy(
        self,
        policy: models.DomainPreActuationPolicy = Depends(get_path_domain_policy),
    ) -> schemas.StandardResponse[schemas.Empty]:
        await policy.delete()
        return schemas.StandardResponse()


@cbv(router)
class DomainResourceRoute:
    domain: models.Domain = Depends(get_path_domain)
    actuation_iface: ActuationInterface = Depends(get_actuation_iface)
    ts_db: AsyncpgTimeseries = Depends(get_ts_db)

    @router.get(
        "/{domain}/resources",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def list_resources(
        self,
    ) -> schemas.StandardListResponse[schemas.ResourceConstraintRead]:
        resources = await models.DomainResourceConstraint.find_many(
            models.DomainResourceConstraint.domain.id == self.domain.id
        ).to_list()
        return schemas.StandardListResponse(
            [
                schemas.ResourceConstraintRead.model_validate(resource.dict())
                for resource in resources
            ]
        )

    @router.post(
        "/{domain}/resources/{entity_id}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def update_resource(
        self,
        entity_id: str = Path(),
        resource_update: schemas.ResourceConstraintUpdate = Body(),
    ) -> schemas.StandardResponse[schemas.ResourceConstraintRead]:
        resource = await models.DomainResourceConstraint.find_one(
            models.DomainResourceConstraint.domain.id == self.domain.id,
            models.DomainResourceConstraint.entity_id == entity_id,
        )
        if resource is None:
            resource = models.DomainResourceConstraint(
                domain=self.domain, entity_id=entity_id, value=resource_update.value
            )
        else:
            resource.value = resource_update.value
        await resource.save()
        return schemas.StandardResponse(
            schemas.ResourceConstraintRead.model_validate(resource.dict())
        )

    @router.delete(
        "/{domain}/resources/{entity_id}",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN))
        ],
    )
    async def delete_resource(
        self, entity_id: str = Path()
    ) -> schemas.StandardResponse[schemas.Empty]:
        resource = await models.DomainResourceConstraint.find_one(
            models.DomainResourceConstraint.domain.id == self.domain.id,
            models.DomainResourceConstraint.entity_id == entity_id,
        )
        if resource is None:
            raise BizError(ErrorCode.ResourceConstraintNotFoundError)
        await resource.delete()
        return schemas.StandardResponse()

    @router.post("/{domain}/resources/{entity_id}/notify")
    async def notify_resource(
        self,
        entity_id: str = Path(),
        resource_update: schemas.ResourceConstraintUpdate = Body(),
    ) -> schemas.StandardResponse[schemas.Empty]:
        resource = await models.DomainResourceConstraint.find_one(
            models.DomainResourceConstraint.domain.id == self.domain.id,
            models.DomainResourceConstraint.entity_id == entity_id,
        )
        if resource is None:
            raise BizError(ErrorCode.ResourceConstraintNotFoundError)
        policy = SchedulingPolicyNaive(self.domain, self.ts_db, self.actuation_iface)
        await policy.schedule(
            schemas.ResourceConstraintRead(
                entity_id=entity_id, value=resource_update.value
            )
        )
        return schemas.StandardResponse()
