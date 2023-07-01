from abc import ABC, abstractmethod
from typing import Any, List

from brick_server.minimal.interfaces.timeseries.asyncpg_timeseries import (
    AsyncpgTimeseries,
)
from loguru import logger

from brick_server.playground import models, schemas


class SchedulingPolicyBase(ABC):
    def __init__(self, domain: models.Domain, ts_db: AsyncpgTimeseries):
        self.domain = domain
        self.ts_db = ts_db

    @abstractmethod
    async def blame(self, location: str, resource_type: str) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    async def find_victim(
        self, history: List[Any], notify_resource: schemas.NotifyResource
    ):
        raise NotImplementedError()

    async def schedule(self, notify_resource: schemas.NotifyResource):
        entity_ids = await self.blame(
            notify_resource.location, notify_resource.resource_type
        )
        # get history with entity_ids (postgres)
        history = await self.ts_db.get_history_data(self.domain.name, entity_ids)
        # result = sorted(result, key=lambda x: x[0])
        # for key, value in itertools.groupby(result, key=lambda x: x[0]):
        #     row = list(map(lambda x: x[1:], value))
        #     logger.info("{}: {}", key, row)
        logger.info(history)
        victim_apps, victim_entity_ids = await self.find_victim(
            history, notify_resource
        )
        logger.info("victim apps: {}", victim_apps)
        logger.info("victim entity_ids: {}", victim_entity_ids)

        # [('additionalProp1', 'admin', 'sb', datetime.datetime(2023, 7, 1, 18, 8, 0, 963859)),
        #  ('additionalProp3', 'admin', 'sb', datetime.datetime(2023, 7, 1, 18, 8, 1, 205563)),
        #  ('additionalProp1', 'admin', 'sb', datetime.datetime(2023, 7, 2, 2, 37, 25))]
