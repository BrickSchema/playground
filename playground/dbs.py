from brick_server.configs import configs

configs['auth']['permission_redis']


async def init_redis():
    pool = await aioredis.create_pool('redis://localhost',
                                      minsize=5,
                                      maxsize=10,
                                      )
    return pool
pool = asyncio.ensure_future(init_redis())

def get_redis_pool():
    return pool


