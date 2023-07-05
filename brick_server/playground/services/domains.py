from typing import Dict, List

from brick_server.minimal.auth.checker import PermissionChecker
from brick_server.minimal.exceptions import AlreadyExistsError, DoesNotExistError
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
)

domain_router = InferringRouter(tags=["Domains"])


@cbv(domain_router)
class DomainAppRoute:
    @domain_router.post("/{domain}/apps/{app}")
    async def add_app(
        self,
        domain: models.Domain = Depends(get_domain),
        app: models.App = Depends(get_app),
    ):
        if not app.approved:
            raise DoesNotExistError("app", app.name)
        domain_app = models.DomainApp(
            domain=domain,
            app=app,
        )
        try:
            domain_app.save()
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("app", app.name)


@cbv(domain_router)
class DomainUserProfileRoute:
    @domain_router.get("/{domain}/user_profiles_arguments")
    async def get_domain_user_profiles(
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
        guard = models.DomainPreActuationPolicy(
            domain=domain,
            **pre_actuation_policy_create.dict(),
        )
        guard.save()
        return schemas.DomainPreActuationPolicy.from_orm(guard)
