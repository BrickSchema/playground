import itertools
from typing import Any, List

from loguru import logger
from sbos.minimal.interfaces import ActuationInterface, AsyncpgTimeseries

from sbos.playground import models, schemas
from sbos.playground.interfaces.app_management import stop_container
from sbos.playground.interfaces.scheduling_policy.base import SchedulingPolicyBase


class SchedulingPolicyNaive(SchedulingPolicyBase):
    async def blame(self, entity_id: str) -> List[str]:
        return ["http://ucsd.edu/ontology/building/Center_Hall#AH-6.WC-ADJ"]

    async def find_victim(
        self, history: List[Any], notify_resource: schemas.ResourceConstraintRead
    ):
        result = sorted(history, key=lambda x: ((x[1], x[2]), x[4]))
        app_latest_use_time = []
        for key, value in itertools.groupby(result, key=lambda x: (x[1], x[2])):
            app_latest_use_time.append((list(value))[-1])
        app_latest_use_time.sort(key=lambda x: x[4])
        victim_app = app_latest_use_time[-1][3]
        victim_entity = app_latest_use_time[-1][0]
        return [victim_app], [victim_entity]

    async def kill_app(self, domain_user_app_id):
        domain_user_app: models.DomainUserApp = await models.DomainUserApp.get(
            domain_user_app_id
        )
        if domain_user_app is not None and domain_user_app.status == schemas.DockerStatus.RUNNING:
            logger.info("kill app: {}", domain_user_app)
            try:
                loop = asyncio.get_running_loop()
                container = await loop.run_in_executor(None, stop_container, domain_user_app.container_id)
                domain_user_app.status = container.status
                await domain_user_app.save()
                return True
            except Exception as e:
                logger.exception(e)

        return False
    async def relinquish_entity(self, entity_id):
        logger.info("relinquish entity: {}", entity_id)
        try:
            await self.actuation_iface.actuate(self.domain, entity_id, "null")
        except Exception as e:
            logger.exception(e)

    async def process_app_and_entity(self, domain_user_app_id, entity_id):
        killed = await self.kill_app(domain_user_app_id)
        if killed:
            await self.relinquish_entity(entity_id)

    async def schedule(self, notify_resource: schemas.ResourceConstraintRead):
        entity_ids = await self.blame(notify_resource.entity_id)
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
        if len(victim_apps) > 0 and len(victim_entity_ids) > 0:
            await self.process_app_and_entity(victim_apps[0], victim_entity_ids[0])

        # await asyncio.gather(
        #     *[self.kill_app(app) for app in victim_apps],
        #     *[self.relinquish_entity(entity_id) for entity_id in victim_entity_ids]
        # )
