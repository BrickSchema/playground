import asyncio
from typing import Literal

from fastapi import APIRouter, Body, Depends, Query
from fastapi_restful.cbv import cbv
from loguru import logger
from sbos.minimal.interfaces import AsyncpgTimeseries, GraphDB
from sbos.minimal.interfaces.cache import clear_cache
from sbos.minimal.securities.checker import PermissionChecker

from sbos.playground import models, schemas
from sbos.playground.utilities.dependencies import (
    get_graphdb,
    get_path_profile,
    get_ts_db,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@cbv(router)
class ProfileRoute:
    checker: PermissionChecker = Depends(
        PermissionChecker(permission_scope=schemas.PermissionScope.DOMAIN)
    )
    graphdb: GraphDB = Depends(get_graphdb)
    ts_db: AsyncpgTimeseries = Depends(get_ts_db)

    # TODO: bind domain and profile
    @router.post("/")
    async def create_profile(
        self,
        profile_create: schemas.PermissionProfileCreate = Body(),
    ) -> schemas.StandardResponse[schemas.PermissionProfileRead]:
        profile = models.PermissionProfile(
            name=profile_create.name,
            read=profile_create.read,
            write=profile_create.write,
            arguments=profile_create.arguments,
        )
        try:
            await profile.save()
        except Exception as e:
            logger.exception(e)
        logger.info(profile.id)
        return schemas.PermissionProfileRead.model_validate(
            profile.dict()
        ).to_response()

    @router.get("/")
    async def list_profiles(
        self,
        type: Literal["app", "user"] = Query("user"),
    ) -> schemas.StandardListResponse[schemas.PermissionProfileRead]:
        profiles = await models.PermissionProfile.find_many(models.PermissionProfile.type == type).to_list()
        return schemas.StandardListResponse(
            results=[
                schemas.PermissionProfileRead.model_validate(profile.dict())
                for profile in profiles
            ]
        )

    @router.get("/{profile}")
    async def get_profile(
        self,
        profile: models.PermissionProfile = Depends(get_path_profile),
    ) -> schemas.StandardResponse[schemas.PermissionProfileRead]:
        return schemas.PermissionProfileRead.model_validate(
            profile.dict()
        ).to_response()

    @router.post("/{profile}")
    async def update_profile(
        self,
        profile: models.PermissionProfile = Depends(get_path_profile),
        profile_update: schemas.PermissionProfileUpdate = Body(...),
    ) -> schemas.StandardResponse[schemas.PermissionProfileRead]:
        profile_update.update_model(profile)
        await profile.save()

        domains = (
            await models.DomainUserProfile.find_many(
                models.DomainUserProfile.profile.id == profile.id,
            )
            .aggregate(
                [
                    {"$group": {"_id": "$domain.$id"}},
                    {
                        "$lookup": {
                            "from": "domains",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "domains",
                        }
                    },
                    {"$replaceRoot": {"newRoot": {"$arrayElemAt": ["$domains", 0]}}},
                ],
                projection_model=models.Domain,
            )
            .to_list()
        )

        jobs = []
        for domain in domains:
            jobs.append(clear_cache(f"{domain.name}:authorized_entities"))
            jobs.append(clear_cache(f"{domain.name}:permission_profile:{profile.id}"))
        await asyncio.gather(*jobs)

        return schemas.PermissionProfileRead.model_validate(
            profile.dict()
        ).to_response()

    # @router.post("/{domain}/test")
    # async def test(
    #     self,
    #     # entity_id: str = Query(..., description=Descriptions.entity_id),
    #     # domain: Domain = Depends(query_domain),
    #     checker: Any = Depends(PermissionCheckerWithEntityId(PermissionType.READ)),
    # ) -> None:
    #     pass
