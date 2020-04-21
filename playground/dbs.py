import redis

from brick_server.configs import configs

##configs['auth']['permission_redis']
#
#
#async def init_redis():
#    pool = await aioredis.create_pool('redis://localhost',
#                                      minsize=5,
#                                      maxsize=10,
#                                      )
#    return pool
#pool = asyncio.ensure_future(init_redis())
#
#def get_redis_pool():
#    return pool


app_management_redis_db = redis.StrictRedis(host=configs['app_management']['redis']['hostname'],
                             port=configs['app_management']['redis']['port'],
                             db=configs['app_management']['redis']['db'],
                             password=configs['app_management']['redis']['password'],
                             decode_responses=True)


def get_app_management_redis_db():
    return app_management_redis_db
