from typing import Type, Union

from brick_server.minimal.config import AuthConfig, BaseConfig, DatabaseConfig
from fastapi_rest_framework import config


@config.add
class RedisConfig(config.Base):
    redis_host: str = "localhost"
    redis_port: int = 5379
    redis_password: str = ""
    redis_dbname: str = "brickserver"


@config.add
class PlaygroundConfig(config.Base):
    default_admin: str = "example@gmail.com"


FastAPIConfig: Type[
    Union[BaseConfig, AuthConfig, DatabaseConfig, RedisConfig, PlaygroundConfig]
] = config.generate_config_class(mixins=[config.EnvFileMixin, config.CLIMixin])
