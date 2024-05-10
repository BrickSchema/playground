from beanie import PydanticObjectId
from brick_server.minimal.securities.auth import get_token_user
from brick_server.minimal.utilities.dependencies import *
from fastapi import Depends

from brick_server.playground import models
from brick_server.playground.interfaces.app_management import app_management_redis_db
from brick_server.playground.utilities.exceptions import ErrorCode


def get_app_management_redis_db():
    return app_management_redis_db


async def get_path_app(app: str = Path(...)) -> models.App:
    if ObjectId.is_valid(app):
        app_model = await models.App.get(app)
    else:
        app_model = await models.App.find_one(models.App.name == app)
    if app_model is None:
        raise BizError(ErrorCode.AppNotFoundError)
    return app_model


async def get_path_domain_user(
    domain: models.Domain = Depends(get_path_domain),
    user: models.User = Depends(get_path_user),
) -> models.DomainUser:
    domain_user_model = await models.DomainUser.find_one(
        models.DomainUser.domain.id == domain.id,
        models.DomainUser.user.id == user.id,
    )
    if domain_user_model is None:
        raise BizError(ErrorCode.DomainUserNotFoundError)
    return domain_user_model


async def get_path_profile(
    profile: PydanticObjectId = Path(
        ..., description="ObjectId of the permission profile"
    )
) -> models.PermissionProfile:
    profile_model = await models.PermissionProfile.get(profile)
    if profile_model is None:
        raise BizError(ErrorCode.DomainNotFoundError)
    return profile_model


async def get_domain_user_profiles(
    domain: models.Domain = Depends(get_path_domain),
    user: models.User = Depends(get_token_user),
) -> list[models.DomainUserProfile]:
    return await models.DomainUserProfile.find_many(
        models.DomainUserProfile.domain.id == domain.id,
        models.DomainUserProfile.user.id == user.id,
        fetch_links=True,
    ).to_list()


async def get_path_domain_policy(
    domain: models.Domain = Depends(get_path_domain),
    policy: PydanticObjectId = Path(
        ..., description="ObjectId of the domain pre actuation policy"
    ),
) -> models.DomainPreActuationPolicy:
    policy_model = await models.DomainPreActuationPolicy.find_one(
        models.DomainPreActuationPolicy.domain.id == domain.id,
        models.DomainPreActuationPolicy.id == policy,
    )
    if policy_model is None:
        raise BizError(ErrorCode.DomainPreActuationPolicyNotFoundError)
    return policy_model
