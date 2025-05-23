import asyncio
import time

from loguru import logger

from sbos.minimal.interfaces.actuation.bacnet import BacnetActuation
from sbos.minimal.interfaces.actuation.base_actuation import BaseActuation
from sbos.minimal.interfaces.actuation.metasys import MetasysActuation
from sbos.minimal.interfaces.cache import use_cache
from sbos.minimal.utilities.exceptions import BizError, ErrorCode
from sbos.minimal.utilities.utils import get_external_references


class ActuationInterface:
    def __init__(self):
        self.actuation_dict = {
            "https://brickschema.org/schema/Brick/ref#BACnetReference": BacnetActuation(),
            "https://brickschema.org/schema/Brick/ref#MetasysReference": MetasysActuation(),
        }

    async def get_actuation_driver(self, external_references) -> BaseActuation:
        types = external_references.getall(
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        )
        for actuation_type in types:
            if actuation_type in self.actuation_dict:
                return self.actuation_dict[actuation_type]
        raise BizError(ErrorCode.ActuationDriverNotFoundError, ",".join(types))

    async def actuate(self, domain, entity_id, value):
        # TODO: get actuation_name in brick graph with cache
        start = time.time()
        driver_time = 0
        actuation_time = 0
        try:
            cache_key = f"{domain.name}:external_references:{entity_id}"
            external_references = await use_cache(
                cache_key, get_external_references, domain, entity_id
            )
            driver = await self.get_actuation_driver(external_references)
            driver_time = time.time() - start  # for benchmark
            start = time.time()
            success, detail = await driver.actuate(
                entity_id, value, external_references
            )
            actuation_time = time.time() - start  # for benchmark
        except Exception as e:
            logger.exception(e)
            success, detail = False, f"{e}"
        return success, detail, driver_time, actuation_time

    async def read(self, domain, entity_id):
        # TODO: get actuation_name in brick graph with cache
        try:
            cache_key = f"{domain.name}:external_references:{entity_id}"
            external_references = await use_cache(
                cache_key, get_external_references, domain, entity_id
            )
            driver = await self.get_actuation_driver(external_references)
            future = driver.read(entity_id, external_references)
            success, detail = await asyncio.wait_for(future, timeout=10)
        except Exception as e:
            success, detail = False, f"{e}"
            logger.exception(e)
        return success, detail
