from functools import lru_cache
from sbos.monitor.config.settings.base import MonitorBaseSettings


@lru_cache()
def get_settings() -> MonitorBaseSettings:
    return MonitorBaseSettings()  # type: ignore


settings: MonitorBaseSettings = get_settings()
