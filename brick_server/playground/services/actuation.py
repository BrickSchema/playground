import asyncio
import time
from typing import List, Optional, Tuple

from brick_server.minimal.interfaces.cache import use_cache
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


async def execute_policy_query(
    self: ActuationEntity,
    domain: models.Domain,
    policy: models.DomainPreActuationPolicy,
):
    res = await self.graphdb.query(domain.name, policy.query)
    parsed_res = parse_graphdb_result(res)
    assert len(parsed_res.keys()) == 1
    entity_ids = parsed_res[list(parsed_res.keys())[0]]
    return entity_ids


async def find_policy(
    self: ActuationEntity, domain: models.Domain, entity_id: str
) -> Optional[models.DomainPreActuationPolicy]:
    policies: List[models.DomainPreActuationPolicy] = list(
        get_docs(models.DomainPreActuationPolicy, domain=domain)
    )
    policies.sort(key=lambda x: -x.priority)
    # TODO: use multiple policies when entity_ids overlapping
    for policy in policies:
        if policy.query:
            cache_key = f"policy_query:{domain.name}:{policy.id}"
            entity_ids = await use_cache(
                cache_key, execute_policy_query, self, domain, policy
            )
            logger.info(entity_id)
            logger.info(entity_id in entity_ids)
            logger.info(len(entity_ids))
            if entity_id not in entity_ids:
                continue
        logger.info("{} {} {}", domain.name, policy.name, entity_id)
        return policy
    return None
    # raise Exception(f"policy not found for entity {entity_id} in domain {domain.name}")


async def guard_before_actuation(
    self: ActuationEntity, domain: models.Domain, entity_id: str, value
) -> Tuple[bool, str, float, float]:
    # logger.info(domain)
    # logger.info(entity_id)
    start = time.time()
    cache_key = f"policy:{domain.name}:{entity_id}"
    policy = await use_cache(cache_key, find_policy, self, domain, entity_id)
    logger.info(policy)
    end = time.time()
    policy_time = end - start
    start = end
    if policy is None:
        return True, "", policy_time, 0
    for guard_name in policy.guards:
        if guard_name not in actuation_guards:
            # use next guard if not found
            logger.warning("{} not found in actuation guards", guard_name)
            continue
        result = None
        try:
            func = actuation_guards[guard_name]
            if hasattr(func, "__call__"):
                func = func.__call__
            if asyncio.iscoroutinefunction(func):
                result = await func(entity_id, value)
            else:
                result = func(entity_id, value)
            result = bool(value)
        except Exception as e:
            # use next guard if the entity_id and value cannot be handled
            logger.exception(e)
            pass
        logger.info("check with {}, result = {}", guard_name, result)
        if result is False:
            detail = "actuate {entity_id} with value {value} blocked by guard {guard_name} in policy {policy.name}"
            return False, detail, policy_time, time.time() - start
        if result is True:
            return True, "", policy_time, time.time() - start
    return True, "", policy_time, time.time() - start


ActuationEntity.guard_before_actuation = guard_before_actuation
