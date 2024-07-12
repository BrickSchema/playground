from sbos.minimal.config.settings.environment import Environment

from sbos.playground.config.settings.base import BackendBaseSettings


class BackendProdSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION
