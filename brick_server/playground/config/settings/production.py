from brick_server.minimal.config.settings.environment import Environment

from brick_server.playground.config.settings.base import BackendBaseSettings


class BackendProdSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION
