from typing import Any

from brick_server.minimal.auth.checker import (
    PermissionCheckerWithEntityId,
    PermissionType,
)
from brick_server.minimal.dependencies import get_graphdb, get_ts_db
from brick_server.minimal.interfaces import AsyncpgTimeseries, GraphDB
from brick_server.minimal.models import get_docs
from fastapi import Body, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger

from brick_server.playground import models, schemas
from brick_server.playground.auth.authorization import get_permission_profile

profile_router = InferringRouter(tags=["Profiles"])


@cbv(profile_router)
class ProfileRoute:
    # auth_logic: Callable = Depends(dependency_supplier.auth_logic)
    graphdb: GraphDB = Depends(get_graphdb)
    ts_db: AsyncpgTimeseries = Depends(get_ts_db)

    @profile_router.post("/")
    async def create_profile(
        self,
        permission_profile_create: schemas.PermissionProfileCreate = Body(),
        # domain: str = Path(...),
        # checker: Any = Depends(PermissionChecker(permission_scope=PermissionScope.SITE)),
    ) -> schemas.PermissionProfile:
        created_profile = models.PermissionProfile(
            read=permission_profile_create.read,
            write=permission_profile_create.write,
        )
        try:
            created_profile.save()
        except Exception:
            pass
        logger.info(created_profile.id)
        return schemas.PermissionProfile.from_orm(created_profile)

    @profile_router.get("/")
    async def list_profiles(self) -> schemas.PermissionProfileList:
        profiles = get_docs(models.PermissionProfile)
        return schemas.PermissionProfileList(
            profiles=[
                schemas.PermissionProfile.from_orm(profile) for profile in profiles
            ]
        )

    @profile_router.get("/{profile}")
    async def get_profile(
        self,
        permission_profile: models.PermissionProfile = Depends(get_permission_profile),
    ) -> schemas.PermissionProfile:
        return schemas.PermissionProfile.from_orm(permission_profile)

    @profile_router.post("/{profile}")
    async def update_profile(
        self,
        permission_profile: models.PermissionProfile = Depends(get_permission_profile),
        permission_profile_update: schemas.PermissionProfileUpdate = Body(...),
    ) -> schemas.PermissionProfile:
        if permission_profile_update.read is not None:
            permission_profile.read = permission_profile_update.read
        if permission_profile_update.write is not None:
            permission_profile.write = permission_profile_update.write
        # d = {k: v for k, v in permission_profile_update.dict().items() if v is not None}
        # permission_profile.__dict__.update(**d)
        permission_profile.save()
        return schemas.PermissionProfile.from_orm(permission_profile)

    @profile_router.post("/{domain}/test")
    async def test(
        self,
        # entity_id: str = Query(..., description=Descriptions.entity_id),
        # domain: Domain = Depends(query_domain),
        checker: Any = Depends(PermissionCheckerWithEntityId(PermissionType.READ)),
    ) -> None:
        pass
