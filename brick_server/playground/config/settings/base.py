import pathlib

from brick_server.minimal.config.settings.base import (
    BackendBaseSettings as MinimalSettings,
)
from pydantic import Field
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()


class BackendPlaygroundSettings(BaseSettings):
    DEFAULT_ADMIN: str = Field(
        default="example@gmail.com",
        description="The email of default admin user. "
        "(deprecated, we should remove it in future version)",
    )
    ISOLATED_NETWORK_NAME: str = Field(
        default="isolated_nw", description="The name of the isolated network in docker."
    )
    DOCKER_PREFIX: str = Field(
        default="brick-server-playground",
        description="The docker prefix to use in app containers.",
    )
    APP_STATIC_DIR: pathlib.Path = Field(
        default="app_static", description="The directory to save app static files."
    )


class BackendBaseSettings(BackendPlaygroundSettings, MinimalSettings):
    TITLE: str = "Brick Server Playground"
    VERSION: str = "0.1.0"

    class Config(MinimalSettings.Config):
        env_file: str = f"{str(ROOT_DIR)}/.env"
