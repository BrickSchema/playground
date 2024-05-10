from brick_server.minimal.config.settings.environment import Environment

from brick_server.playground.config.settings.base import BackendBaseSettings


class BackendStageSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Test Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.STAGING
