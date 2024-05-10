import pathlib

import decouple
from brick_server.minimal.config.settings.base import (
    BackendBaseSettings as BaseSettings,
)

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "Brick Server Playground"
    VERSION: str = "0.1.0"

    DEFAULT_ADMIN: str = decouple.config(
        "DEFAULT_ADMIN", cast=str, default="example@gmail.com"
    )
    ISOLATED_NETWORK_NAME: str = decouple.config(
        "ISOLATED_NETWORK_NAME", cast=str, default="isolated_nw"
    )
    DOCKER_PREFIX: str = decouple.config(
        "DOCKER_PREFIX", cast=str, default="brick-server-playground"
    )
    APP_STATIC_DIR: str = decouple.config(
        "APP_STATIC_DIR", cast=str, default=str(pathlib.Path("app_static").resolve())
    )

    class Config(BaseSettings.Config):
        env_file: str = f"{str(ROOT_DIR)}/.env"
