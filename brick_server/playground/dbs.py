import redis
from aiocache import caches
from fastapi_rest_framework.config import settings

from brick_server.playground.models import (
    DomainOccupancy,
    DomainPreActuationPolicy,
    DomainUser,
    DomainUserProfile,
    PermissionProfile,
    User,
)

# from brick_server.configs import configs

# configs['auth']['permission_redis']
#
#
# async def init_redis():
#    pool = await aioredis.create_pool('redis://localhost',
#                                      minsize=5,
#                                      maxsize=10,
#                                      )
#    return pool
# pool = asyncio.ensure_future(init_redis())
#
# def get_redis_pool():
#    return pool

caches.set_config(
    {
        "default": {
            "cache": "aiocache.RedisCache",
            "endpoint": settings.redis_host,
            "port": settings.redis_port,
            "db": settings.redis_db,
            "password": settings.redis_password,
            "timeout": 1,
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            "plugins": [
                {"class": "aiocache.plugins.HitMissRatioPlugin"},
                {"class": "aiocache.plugins.TimingPlugin"},
            ],
        }
    }
)


app_management_redis_db = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
    decode_responses=True,
)


def get_app_management_redis_db():
    return app_management_redis_db


def init_mongodb():
    for model in [
        PermissionProfile,
        User,
        DomainUser,
        DomainOccupancy,
        DomainUserProfile,
        DomainPreActuationPolicy,
    ]:
        model.ensure_indexes()
