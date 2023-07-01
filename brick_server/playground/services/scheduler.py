from fastapi import Body, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from brick_server.playground import models, schemas
from brick_server.playground.auth.authorization import get_domain

scheduler_router = InferringRouter(tags=["Scheduler"])


@cbv(scheduler_router)
class NotifyResourceRoute:
    @scheduler_router.post("/domains/{domain}/notify_resource")
    async def notify_resource(
        self,
        domain: models.Domain = Depends(get_domain),
        body: schemas.NotifyResource = Body(),
    ):
        pass
