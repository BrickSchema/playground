from sbos.minimal.config.settings.environment import Environment

from sbos.playground.config.settings.base import BackendBaseSettings


class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
