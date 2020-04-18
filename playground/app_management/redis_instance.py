import redis
from ..configs import configs

redis_host = "localhost"
redis_port = 6379
redis_password = ""

redis_db = redis.StrictRedis(host=configs['auth_server']['hostname'],
                             port=configs['auth_server']['port'],
                             db=configs['auth_server']['instance_db'],
                             password=configs['auth_server']['password'],
                             decode_responses=True)
