from typing import Type, Union

from brick_server.minimal.config import AuthConfig, BaseConfig, DatabaseConfig
from fastapi_rest_framework import config


@config.add
class RedisConfig(config.Base):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = "brick-demo"
    redis_db: int = 0


@config.add
class PlaygroundConfig(config.Base):
    default_admin: str = "example@gmail.com"
    isolated_network_name: str = "isolated_nw"
    docker_prefix: str = "brick-server-playground"
    # cache: bool = False
    cache: bool = True


FastAPIConfig: Type[
    Union[BaseConfig, AuthConfig, DatabaseConfig, RedisConfig, PlaygroundConfig]
] = config.generate_config_class(mixins=[config.EnvFileMixin, config.CLIMixin])
