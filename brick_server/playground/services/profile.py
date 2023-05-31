from typing import Any, Callable

from fastapi import BackgroundTasks, Depends, File, Path, UploadFile, Query
from fastapi_rest_framework.config import settings
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger

from brick_server.playground import models, schemas
from brick_server.minimal.auth.authorization import PermissionChecker, PermissionType, PermissionCheckerWithEntityId, \
    create_user
from brick_server.minimal.dependencies import (
    dependency_supplier,
    get_graphdb,
    get_ts_db,
    path_domain, query_domain,
)
from brick_server.minimal.descriptions import Descriptions
from brick_server.minimal.exceptions import AlreadyExistsError
from brick_server.minimal.interfaces import AsyncpgTimeseries, GraphDB
from brick_server.minimal.schemas import IsSuccess, Domain


profile_router = InferringRouter(tags=["Profiles"])


@cbv(profile_router)
class ProfileRoute:
    auth_logic: Callable = Depends(dependency_supplier.auth_logic)
    graphdb: GraphDB = Depends(get_graphdb)
    ts_db: AsyncpgTimeseries = Depends(get_ts_db)

    @profile_router.post("/create")
    async def create_profile(
            self,
            # background_tasks: BackgroundTasks,
            # domain: str = Path(...),
            # checker: Any = Depends(PermissionChecker(PermissionType.write)),
    ) -> schemas.PermissionProfile:
        # create_user("admin", "admin", "admin@gmail.com")

        created_profile = models.PermissionProfile(read="", write="")
        try:
            created_profile.save()
        except Exception:
            pass
            # raise AlreadyExistsError("domain", "name")
        return schemas.PermissionProfile.from_orm(created_profile)

    @profile_router.post("/{domain}/test")
    async def test(
            self,
            # entity_id: str = Query(..., description=Descriptions.entity_id),
            # domain: Domain = Depends(query_domain),
            checker: Any = Depends(PermissionCheckerWithEntityId(PermissionType.read)),
    ) -> None:
        pass
