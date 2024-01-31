from typing import Dict, List

from brick_server.minimal.auth.checker import PermissionChecker
from brick_server.minimal.exceptions import AlreadyExistsError, DoesNotExistError
from brick_server.minimal.models import get_doc, get_doc_or_none, get_docs
from brick_server.minimal.schemas import PermissionScope
from fastapi import Body, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from brick_server.playground import models, schemas
from brick_server.playground.auth.authorization import (
    Authorization,
    get_app,
    get_domain,
    get_domain_user_profiles,
    get_user,
)

domain_router = InferringRouter(tags=["Domains"])


@cbv(domain_router)
class DomainAppRoute:
    @domain_router.post("/{domain}/apps/{app}")
    async def add_app(
        self,
        domain: models.Domain = Depends(get_domain),
        app: models.App = Depends(get_app),
    ) -> schemas.DomainApp:
        if not app.approved:
            raise DoesNotExistError("app", app.name)
        domain_app = models.DomainApp(
            domain=domain,
            app=app,
        )
        try:
            domain_app.save()
            return schemas.DomainApp.from_orm(domain_app)
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("app", app.name)


@cbv(domain_router)
class DomainUserRoute:
    @domain_router.post("/{domain}/users/{user}")
    async def add_domain_user(
        self,
        domain: models.Domain = Depends(get_domain),
        user: models.User = Depends(get_user),
    ) -> schemas.DomainUser:
        domain_user = models.DomainUser(domain=domain, user=user)
        try:
            domain_user.save()
            return schemas.DomainUser.from_orm(domain_user)
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("domain_user", user.user_id)


@cbv(domain_router)
class DomainUserProfileRoute:
    @domain_router.post("/{domain}/users/{user}/profiles")
    async def update_domain_user_profile(
        self,
        domain: models.Domain = Depends(get_domain),
        user: models.User = Depends(get_user),
        domain_user_profile_update: schemas.DomainUserProfileUpdate = Body(),
    ) -> schemas.DomainUserProfile:
        domain_user = get_doc(models.DomainUser, domain=domain, user=user)
        profile = get_doc(
            models.PermissionProfile, id=domain_user_profile_update.profile
        )
        domain_user_profile = get_doc_or_none(
            models.DomainUserProfile, domain=domain, user=user, profile=profile
        )
        if domain_user_profile is None:
            domain_user_profile = models.DomainUserProfile(
                domain=domain,
                user=user,
                profile=profile,
                arguments=domain_user_profile_update.arguments,
            )
        else:
            domain_user_profile.arguments = domain_user_profile_update.arguments
        try:
            domain_user_profile.save()
            return schemas.DomainUserProfile.from_orm(domain_user_profile)
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("domain_user", user.user_id)

    @domain_router.get("/{domain}/users/{user}/profiles")
    async def list_domain_user_profile(
        self,
        domain: models.Domain = Depends(get_domain),
        user: models.User = Depends(get_user),
    ) -> schemas.DomainUserProfileList:
        domain_user_profiles = get_docs(
            models.DomainUserProfile, domain=domain, user=user
        )
        return schemas.DomainUserProfileList(
            profiles=[
                schemas.DomainUserProfile.from_orm(profile)
                for profile in domain_user_profiles
            ]
        )

    @domain_router.get("/{domain}/user_profiles_arguments")
    async def get_domain_user_profiles_arguments(
        self,
        profiles: List[models.DomainUserProfile] = Depends(get_domain_user_profiles),
        checker: Authorization = Depends(
            PermissionChecker(permission_scope=PermissionScope.ENTITY)
        ),
    ) -> List[Dict[str, str]]:
        return [profile.arguments for profile in profiles]


@cbv(domain_router)
class DomainPreActuationPolicy:
    @domain_router.post("/{domain}/pre_actuation_policy")
    async def create_pre_actuation_policy(
        self,
        domain: models.Domain = Depends(get_domain),
        pre_actuation_policy_create: schemas.DomainPreActuationPolicyCreate = Body(...),
    ) -> schemas.DomainPreActuationPolicy:
        policy = models.DomainPreActuationPolicy(
            domain=domain,
            **pre_actuation_policy_create.dict(),
        )
        policy.save()
        return schemas.DomainPreActuationPolicy.from_orm(policy)

    @domain_router.delete("/{domain}/pre_actuation_policy")
    async def delete_pre_actuation_policy(
        self,
        domain: models.Domain = Depends(get_domain),
    ):
        policies = get_docs(models.DomainPreActuationPolicy, domain=domain)
        for policy in policies:
            policy.delete()
