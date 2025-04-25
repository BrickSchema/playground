import asyncio
from abc import ABC, abstractmethod
from typing import Any, List

from loguru import logger
from sbos.minimal.interfaces import ActuationInterface, AsyncpgTimeseries

from sbos.playground import models, schemas


class SchedulingPolicyBase(ABC):
    def __init__(
        self,
        domain: models.Domain,
        ts_db: AsyncpgTimeseries,
        actuation_iface: ActuationInterface,
    ):
        self.domain = domain
        self.ts_db = ts_db
        self.actuation_iface = actuation_iface

    @abstractmethod
    async def blame(self, entity_id: str) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    async def find_victim(
        self, history: List[Any], notify_resource: schemas.ResourceConstraintRead
    ):
        raise NotImplementedError()

    @abstractmethod
    async def schedule(self, notify_resource: schemas.ResourceConstraintRead):
        raise NotImplementedError()
