import asyncio
import multiprocessing
import time
from collections import defaultdict
import json

import httpx
import pydantic
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger

from sbos.monitor.config.manager import settings

mongo_uri: pydantic.MongoDsn = pydantic.MongoDsn(
    url=f"{settings.MONGO_SCHEMA}://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}",
)
mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(str(mongo_uri), uuidRepresentation="standard")
mongo_database: AsyncIOMotorDatabase = mongo_client[settings.MONGO_DATABASE]
playground_api_base = f"http://{settings.PLAYGROUND_HOST}:{settings.PLAYGROUND_PORT}/brickapi/v1"


async def validate_resources_in_domain(domain, domain_data):
    logger.info("Validate resources in {}", domain)
    constraint_map = {}
    for data in domain_data:
        entity_id = data["entity_id"]
        value = data["value"]
        constraint_map[entity_id] = value
    async with httpx.AsyncClient() as client:
        violated_constraints = {}
        url = f"{playground_api_base}/actuation/domains/{domain}/read"
        data = {k: [""] for k, v in constraint_map.items()}
        headers = {"Authorization": f"Bearer {settings.PLAYGROUND_JWT_TOKEN}"}
        response = await client.post(url, json=data, headers=headers)
        response_dict = response.json()
        if response_dict["errorCode"] == "Success":
            results = response_dict["data"]["results"]
            logger.info("Actuation results: {}", results)

            for result in results:
                entity_id = result["entityId"]
                if entity_id not in constraint_map:
                    logger.error("Actuate read failed: unknown entity {}", entity_id)
                    continue
                if result["success"] is False:
                    logger.error("Actuate read failed: {} {}", entity_id, result["detail"])
                    continue
                real_value = float(result["detail"])
                if real_value > constraint_map[entity_id]:
                    logger.info("Actuate read violated: {} {} > {}", entity_id, real_value, constraint_map[entity_id])
                    violated_constraints[entity_id] = real_value
        else:
            logger.error(response)

        if len(violated_constraints) > 0:
            url = f"{playground_api_base}/domains/{domain}/resources"
            data = {k: [str(v)] for k, v in violated_constraints.items()}
            response = await client.post(url, json=data, headers=headers)
            response_dict = response.json()
            logger.info("Notify result: {}", response_dict)


async def get_resources_constraints():
    res = await mongo_database["domain.resources"].find().to_list()
    logger.info(res)
    domain_map = defaultdict(list)
    for data in res:
        domain = data["domain"].id
        domain_map[domain].append(data)

    tasks = []
    for domain, domain_data in domain_map.items():
        tasks.append(validate_resources_in_domain(domain, domain_data))
    await asyncio.gather(*tasks)


async def polling_async():
    logger.info("Polling started")
    await get_resources_constraints()
    logger.info("Polling ended")


def polling():
    asyncio.run(polling_async())


def main():
    while True:
        try:
            start = time.time()
            p = multiprocessing.Process(target=polling)
            p.start()
            p.join(timeout=settings.POLLING_INTERVAL)
            if p.is_alive():
                p.kill()
            end = time.time()
            wait_time = max(0., settings.POLLING_INTERVAL - (end - start))
            if wait_time > 0:
                logger.info("Wait for {} seconds...", wait_time)
                time.sleep(wait_time)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
