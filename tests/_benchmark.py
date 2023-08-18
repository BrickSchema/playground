import asyncio
import json

import httpx
from fastapi_rest_framework.config import init_settings

from brick_server.playground.config import FastAPIConfig

init_settings(FastAPIConfig)
from brick_server.minimal.auth.jwt import create_jwt_token


async def benchmark(url, method, headers, data=None, iterations=1, test_name=""):
    total_time = 0
    async with httpx.AsyncClient(
        headers=headers, base_url="http://127.0.0.1:9000"
    ) as client:
        for i in range(iterations):
            response = await client.request(method, url, json=data)
            # print(response.text)
            result = json.loads(response.text)
            response_time = result["response_time"]
            total_time += response_time
            # print(result)
    print(test_name, total_time / iterations)


async def run(domain, data, iterations=100):
    print(domain)
    user_jwt = create_jwt_token(user_id="admin", app_name="sb", domain=domain)
    headers = {"Authorization": "Bearer " + user_jwt}
    await benchmark(
        f"/brickapi/v1/user/domains/{domain}/permissions",
        "GET",
        headers,
        test_name="permission",
        iterations=iterations,
    )
    await benchmark(
        f"/brickapi/v1/actuation/domains/{domain}",
        "POST",
        headers,
        data,
        test_name="actuation",
        iterations=iterations,
    )


async def main():
    await run("bldg", data={"bldg:BLDG_RM101_ZNT_SP": [16]})

    await run(
        "ebu3b",
        data={"http://ucsd.edu/building/ontology/ebu3b#EBU3B_RM_2150_SUPFLO_SP": [16]},
    )


if __name__ == "__main__":
    asyncio.run(main())
