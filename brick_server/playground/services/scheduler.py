from brick_server.minimal.dependencies import get_ts_db
from brick_server.minimal.interfaces.timeseries.asyncpg_timeseries import (
    AsyncpgTimeseries,
)
from fastapi import Body, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from brick_server.playground import models, schemas
from brick_server.playground.auth.authorization import get_domain
from brick_server.playground.scheduling_policy.naive import SchedulingPolicyNaive

scheduler_router = InferringRouter(tags=["Scheduler"])


@cbv(scheduler_router)
class NotifyResourceRoute:
    ts_db: AsyncpgTimeseries = Depends(get_ts_db)

    @scheduler_router.post("/domains/{domain}/notify_resource")
    async def notify_resource(
        self,
        domain: models.Domain = Depends(get_domain),
        body: schemas.NotifyResource = Body(),
    ):
        policy = SchedulingPolicyNaive(domain, self.ts_db)
        await policy.schedule(body)
