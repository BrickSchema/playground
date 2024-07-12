from functools import lru_cache

import decouple
from loguru import logger
from sbos.minimal.config.settings.environment import Environment

from sbos.playground.config.settings.base import BackendBaseSettings
from sbos.playground.config.settings.development import BackendDevSettings
from sbos.playground.config.settings.production import BackendProdSettings
from sbos.playground.config.settings.staging import BackendStageSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BackendBaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            logger.info("Running in DEVELOPMENT mode")
            return BackendDevSettings()
        elif self.environment == Environment.STAGING.value:
            logger.info("Running in STAGING mode")
            return BackendStageSettings()
        logger.info("Running in PRODUCTION mode")
        return BackendProdSettings()


@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: BackendBaseSettings = get_settings()
