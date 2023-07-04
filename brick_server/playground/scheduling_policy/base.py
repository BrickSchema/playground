import asyncio
from abc import ABC, abstractmethod
from typing import Any, List

from brick_server.minimal.interfaces import ActuationInterface, AsyncpgTimeseries
from brick_server.minimal.models import get_doc_or_none
from loguru import logger

from brick_server.playground import models, schemas
from brick_server.playground.app_management.app_management import stop_container


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
    async def blame(self, location: str, resource_type: str) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    async def find_victim(
        self, history: List[Any], notify_resource: schemas.NotifyResource
    ):
        raise NotImplementedError()

    async def kill_app(self, domain_user_app_id):
        domain_user_app: models.DomainUserApp = get_doc_or_none(
            models.DomainUserApp, id=domain_user_app_id
        )
        if domain_user_app is not None:
            logger.info("kill app: {}", domain_user_app)
            try:
                stop_container(domain_user_app.container_id)
            except Exception as e:
                logger.exception(e)

    async def relinquish_entity(self, entity_id):
        logger.info("relinquish entity: {}", entity_id)
        try:
            self.actuation_iface.actuate(entity_id, "null")
        except Exception as e:
            logger.exception(e)

    async def schedule(self, notify_resource: schemas.NotifyResource):
        entity_ids = await self.blame(
            notify_resource.location, notify_resource.resource_type
        )
        # get history with entity_ids (postgres)
        history = await self.ts_db.get_history_data(self.domain.name, entity_ids)
        # [('additionalProp1', 'admin', 'sb', datetime.datetime(2023, 7, 1, 18, 8, 0, 963859)),
        #  ('additionalProp3', 'admin', 'sb', datetime.datetime(2023, 7, 1, 18, 8, 1, 205563)),
        #  ('additionalProp1', 'admin', 'sb', datetime.datetime(2023, 7, 2, 2, 37, 25))]
        logger.info(history)
        victim_apps, victim_entity_ids = await self.find_victim(
            history, notify_resource
        )
        logger.info("victim apps: {}", victim_apps)
        logger.info("victim entity_ids: {}", victim_entity_ids)
        await asyncio.gather(
            *[self.kill_app(app) for app in victim_apps],
            *[self.relinquish_entity(entity_id) for entity_id in victim_entity_ids]
        )
