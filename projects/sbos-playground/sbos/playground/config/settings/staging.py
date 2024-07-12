from sbos.minimal.config.settings.environment import Environment

from sbos.playground.config.settings.base import BackendBaseSettings


class BackendStageSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Test Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.STAGING
