from typing import Type, Union

from brick_server.minimal.config import AuthConfig, BaseConfig, DatabaseConfig
from fastapi_rest_framework import config


@config.add
class PlaygroundConfig(config.Base):
    default_admin: str = "example@gmail.com"
    isolated_network_name: str = "isolated_nw"
    docker_prefix: str = "brick-server-playground"


FastAPIConfig: Type[
    Union[BaseConfig, AuthConfig, DatabaseConfig, PlaygroundConfig]
] = config.generate_config_class(mixins=[config.EnvFileMixin, config.CLIMixin])
