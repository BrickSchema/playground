from typing import List

from brick_server.minimal.models import get_docs
from brick_server.minimal.services.actuation import (
    ActuationEntity,
    actuation_router as actuation_router,
)
from loguru import logger

from brick_server.playground import models
from brick_server.playground.interface.actuation_guards import actuation_guards
from brick_server.playground.utils import parse_graphdb_result

_ = actuation_router


async def guard_before_actuation(
    self: ActuationEntity, domain: models.Domain, entity_id: str, value
) -> None:
    # logger.info(domain)
    # logger.info(entity_id)
    policies: List[models.DomainPreActuationPolicy] = list(
        get_docs(models.DomainPreActuationPolicy, domain=domain)
    )
    policies.sort(key=lambda x: -x.priority)
    for policy in policies:
        logger.info("{} {} {}", policy.name, entity_id, value)
        if policy.query:
            # TODO: cache in redis
            res = await self.graphdb.query(domain.name, policy.query)
            parsed_res = parse_graphdb_result(res)
            assert len(parsed_res.keys()) == 1
            entity_ids = parsed_res[list(parsed_res.keys())[0]]
            # logger.info(entity_ids)
            if entity_id not in entity_ids:
                continue
        for guard_name in policy.guards:
            if guard_name not in actuation_guards:
                # use next guard if not found
                continue
            result = None
            try:
                result = bool(actuation_guards[guard_name](entity_id, value))
            except Exception:
                # use next guard if the entity_id and value cannot be handled
                pass
            logger.info("check with {}, result = {}", guard_name, result)
            if result is False:
                raise Exception(
                    f"actuate {entity_id} with value {value} blocked by guard {guard_name} in policy {policy.name}"
                )
            if result is True:
                return


ActuationEntity.guard_before_actuation = guard_before_actuation
