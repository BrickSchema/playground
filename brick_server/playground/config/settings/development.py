from brick_server.minimal.config.settings.environment import Environment

from brick_server.playground.config.settings.base import BackendBaseSettings


class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
