from enum import Enum

from brick_server.minimal.schemas.base import StrEnumMixin


class DockerStatus(StrEnumMixin, Enum):
    """
    The states defined in docker documentation (https://docs.docker.com/engine/reference/commandline/ps/)
    """

    CREATED = "created"
    RESTARTING = "restarting"
    RUNNING = "running"
    REMOVING = "removing"
    PAUSED = "paused"
    EXITED = "exited"
    DEAD = "dead"
