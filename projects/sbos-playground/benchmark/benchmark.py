import asyncio
import os
from pathlib import Path

import click
import httpx
import numpy as np
from fastapi_rest_framework.config import init_settings
from loguru import logger
from tenacity import retry, stop_after_delay, wait_exponential
from tqdm import tqdm

from sbos.playground.config import FastAPIConfig

init_settings(FastAPIConfig)
from sbos.minimal.auth.authorization import create_user as brick_create_user
from sbos.minimal.auth.jwt import create_jwt_token
from sbos.minimal.dbs import mongo_connection

_ = mongo_connection
from sbos.minimal.models import get_doc_or_none

from sbos.playground.dbs import init_mongodb
from sbos.playground.models import App, Domain, User

"""global config"""
API_BASE = "http://127.0.0.1:9000/brickapi/v1"
REDIS_API_BASE = "http://redis-commander:8081"
GRAPHDB_API_BASE = "http://graphdb:7200"
DOMAIN_NAME = "Center_Hall"
APP_NAME = "genie"
PROJECT_FOLDER = Path(__file__).parent.parent.absolute()
EXAMPLES_DATA_FOLDER = PROJECT_FOLDER / "examples" / "data"

logger.remove()
logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)


"""util func"""


def test_deco(name):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger.info("---------- Begin {} Microbenchmark ----------", name)
            returned_value = await func(*args, **kwargs)
            logger.info("----------  End {} Microbenchmark  ----------", name)
            return returned_value

        return wrapper

    return decorator


def read_file(filename):
    file = EXAMPLES_DATA_FOLDER / filename
    _entities = set()
    with file.open("r") as f:
        for line in f:
            _entities.add(line.strip())
            # _entities.add(line.strip().replace("http://ucsd.edu/ontology/building/Center_Hall#", "Center_Hall:"))
    return _entities


ENTITIES = list(read_file("center_hall.txt"))
ROOMS = list(read_file("center_hall_rooms.txt"))


"""microbenchmark configurations"""
# number of profiles used in capability derivation test
MAX_PROFILES = 5

# number of users used in capability derivation test
MAX_USERS = 1000

# Permission profile for capability derivation microbenchmark
query_app_read = """
SELECT ?p WHERE {{
?vav a brick:VAV.
?vav brick:feeds {room}.
?vav brick:hasPoint
?p. ?p a ?o.
FILTER (?o IN      (brick:Temperature_Sensor, brick:Occupancy_Sensor, brick:Temperature_Setpoint)).
}}
"""

query_app_write = """
SELECT ?p WHERE {{
?vav a brick:VAV.
?vav brick:feeds {room}.
?vav brick:hasPoint ?p.
?p a ?o.
FILTER (?o IN      (brick:Warm_Cool_Adjust_Sensor, brick:Temperature_Setpoint)).
}}
"""

# Validator assignment policies (Fig.10)

# "Default"
query_default = """
select distinct ?equip where {
    ?equip a brick:Point .
}
    """

# "First Floor"
query_1 = """
select distinct ?p where {
    ?loc brick:isPartOf Center_Hall:First_Floor .
    ?equip brick:feeds ?loc .
    ?p brick:isPointOf ?equip.
}
"""

# "AH-4"
query_2 = """
select distinct ?p where {
    {?p a brick:Point .
    ?p brick:isPointOf ?equip.
        Center_Hall:AH-4 brick:feeds ?equip .}
    UNION
    {?p a brick:Point .
    ?p brick:isPointOf Center_Hall:AH-4.}
}
"""

# "VAV-2"
query_3 = """
select distinct ?p where {
    ?p a brick:Point .
    ?p brick:isPointOf Center_Hall:VAV-2.
}
    """

# "Third Floor"
query_4 = """
select distinct ?p where {
    ?loc brick:isPartOf Center_Hall:Third_Floor .
    ?equip brick:feeds* ?loc .
    ?p brick:isPointOf ?equip.
}
"""


"""
Measurement unit for each microbenchmark
"""


async def benchmark(
    url,
    method,
    headers,
    iterations=1,
    description="",
    warmup=False,
    generate_data=False,
    random_data=False,
    response_key=None,
):
    total_time = 0
    total_iterations = 0
    samples = np.arange(0, len(ENTITIES))
    np.random.shuffle(samples)
    if warmup:
        logger.info("Precomputing Cache...")
    else:
        logger.info("Starting actual tests...")
    async with httpx.AsyncClient(base_url=API_BASE) as client:
        for i in tqdm(range(iterations)):
            # for test 2-4
            if generate_data:
                if random_data:
                    index = samples[i]
                else:
                    index = i
                data = {ENTITIES[index]: [16]}
                _headers = headers
            # for test 1
            else:
                data = None
                _headers = headers[i % len(headers)]
            response = await client.request(method, url, json=data, headers=_headers)
            # logger.info(response.content)
            result = response.json()
            response_time = result["response_time"]
            if response_key is not None:
                response_time = response_time[response_key]
            if iterations * 0.25 <= i < iterations * 0.75:
                total_time += response_time
                total_iterations += 1

    if not warmup:
        logger.info("{}: {} ms", description, total_time / total_iterations)


async def create_domain_pre_actuation_policy(
    domain, name, query, priority, guards=None
):
    # delete all cache in redis
    async with httpx.AsyncClient(base_url=REDIS_API_BASE) as client:
        await client.request(
            "POST", "/apiv2/keys/R%3Aredis%3A6379%3A0/policy%3A*?action=delete"
        )

    user_jwt = create_jwt_token(user_id="admin", app_name=APP_NAME, domain=domain)
    headers = {"Authorization": "Bearer " + user_jwt}
    data = {
        "name": name,
        "query": query,
        "priority": priority,
        "guards": guards if guards is not None else [],
    }
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        await client.request(
            "POST", f"/domains/{domain}/pre_actuation_policy", json=data
        )


async def delete_domain_pre_actuation_policy(domain):
    user_jwt = create_jwt_token(user_id="admin", app_name=APP_NAME, domain=domain)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        await client.request("DELETE", f"/domains/{domain}/pre_actuation_policy")


"""
Execution wrapper for test 1
"""


async def run_1(domain, profile_num, description, iterations=100, warmup=False):
    # print(domain, user)
    user_headers = []
    for i in range(profile_num - 1, MAX_USERS, MAX_PROFILES):
        user_jwt = create_jwt_token(
            user_id=f"user{i}", app_name=APP_NAME, domain=domain
        )
        headers = {"Authorization": "Bearer " + user_jwt}
        user_headers.append(headers)
    if warmup:
        await benchmark(
            f"/user/domains/{domain}/permissions",
            "GET",
            user_headers,
            warmup=True,
            description=description,
            iterations=len(user_headers),
        )
    await benchmark(
        f"/user/domains/{domain}/permissions",
        "GET",
        user_headers,
        description=description,
        iterations=iterations,
    )


"""
Execution wrapper for test 2 - 4
"""


async def run_2(
    domain, description, iterations=100, warmup=False, response_key="policy"
):
    # print(domain, name)
    user_jwt = create_jwt_token(user_id="admin", app_name=APP_NAME, domain=domain)
    headers = {"Authorization": "Bearer " + user_jwt}

    if warmup:
        await benchmark(
            f"/actuation/domains/{domain}",
            "POST",
            headers,
            description=description,
            warmup=True,
            iterations=1344,
            generate_data=True,
            random_data=False,
            response_key=response_key,
        )

    await benchmark(
        f"/actuation/domains/{domain}",
        "POST",
        headers,
        description=description,
        iterations=iterations,
        generate_data=True,
        random_data=True,
        response_key=response_key,
    )


@test_deco("Capability Derivation")
async def test_1(iterations=1000, warmup=False):
    for i in range(1, MAX_PROFILES + 1):
        await run_1(
            domain=DOMAIN_NAME,
            profile_num=i,
            description=f"user assigned with {i} permission profile(s)",
            iterations=iterations,
            warmup=warmup,
        )


@test_deco("Validator Mapping")
async def test_2(iterations=1000, warmup=False):
    await delete_domain_pre_actuation_policy(DOMAIN_NAME)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "default", query_default, 0)
    description = "validator assigned = Default"
    await run_2(DOMAIN_NAME, description, iterations, warmup=warmup)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "FF", query_1, 1)
    description += " + First Floor"
    await run_2(DOMAIN_NAME, description, iterations, warmup=warmup)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "VAV-AHU", query_2, 2)
    description += " + AH-4"
    await run_2(DOMAIN_NAME, description, iterations, warmup=warmup)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "VAV", query_3, 3)
    description += " + VAV-2"
    await run_2(DOMAIN_NAME, description, iterations, warmup=warmup)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "TF", query_4, 4)
    description += " + Third Floor"
    await run_2(DOMAIN_NAME, description, iterations, warmup=warmup)


@test_deco("Resource Specification Retrieval")
async def test_3(iterations=1000, warmup=False):
    await delete_domain_pre_actuation_policy(DOMAIN_NAME)
    await create_domain_pre_actuation_policy(
        DOMAIN_NAME, "default", query_default, 0, ["ml"]
    )
    await run_2(
        DOMAIN_NAME,
        "average time consumption",
        iterations,
        warmup=warmup,
        response_key="guard",
    )


@test_deco("Range Checker")
async def test_4(iterations=1000, warmup=False):
    await delete_domain_pre_actuation_policy(DOMAIN_NAME)
    await create_domain_pre_actuation_policy(
        DOMAIN_NAME, "default", query_default, 0, ["range_checker"]
    )
    await run_2(
        DOMAIN_NAME,
        "average time consumption",
        iterations,
        warmup=warmup,
        response_key="guard",
    )


@test_deco("Power Predictor")
async def test_5(iterations=1000, warmup=False):
    await delete_domain_pre_actuation_policy(DOMAIN_NAME)
    await create_domain_pre_actuation_policy(DOMAIN_NAME, "default", query_default, 0)
    await run_2(
        DOMAIN_NAME,
        "average time consumption",
        iterations,
        warmup=warmup,
        response_key="driver",
    )


def reset_mongodb():
    from mongoengine import connect as mongo_connect

    from sbos.playground.config.manager import settings

    logger.info("Reset database")
    db = mongo_connect(
        host=settings.mongo_host,
        port=settings.mongo_port,
        username=settings.mongo_username,
        password=settings.mongo_password,
        db=settings.mongo_dbname,
        connect=False,
    )
    db.drop_database(settings.mongo_dbname)
    init_mongodb()


async def check_import_schema(repository: str, name: str) -> bool:
    async with httpx.AsyncClient(base_url=GRAPHDB_API_BASE) as client:
        resp = await client.get(f"/rest/data/import/upload/{repository}", timeout=30)
        data = resp.json()
        for row in data:
            if row.get("name", None) == name:
                if row.get("status", None) == "DONE":
                    return True
                return False
        return False


@retry(stop=stop_after_delay(600), wait=wait_exponential(multiplier=1, max=5))
async def ensure_graphdb_upload(repository: str, name: str) -> None:
    try:
        result = await check_import_schema(repository, name)
        assert result
    except Exception as e:
        logger.info("Check import schema failed, retrying...")
        raise e
    logger.info("Check import schema succeeded")


def create_user(user_id, is_admin=False):
    user = get_doc_or_none(User, user_id=user_id)
    if user is None:
        brick_create_user(
            name=user_id,
            user_id=user_id,
            email=f"{user_id}@gmail.com",
            is_admin=is_admin,
        )
        logger.info("User created: {}", user_id)
    else:
        logger.info("User exists: {}", user_id)


async def create_app(app_name):
    user_jwt = create_jwt_token(user_id="admin")
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        app = get_doc_or_none(App, name=app_name)
        if app is None:
            data = {
                "name": app_name,
                "description": "",
                "profile": {"read": query_app_read, "write": query_app_write},
            }
            resp = await client.post(
                f"{API_BASE}/apps",
                headers=headers,
                json=data,
                follow_redirects=True,
            )

            if resp.status_code != 200:
                logger.error("{} {}", resp, resp.request)
                exit(-1)

            logger.info("App created: {}", app_name)
        else:
            logger.info("App exists: {}", app_name)

        resp = await client.post(
            f"{API_BASE}/admin/apps/{app_name}/approve",
            headers=headers,
        )
        if resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        logger.info("App approved: {}", app_name)


async def create_domain(domain_name):
    user_jwt = create_jwt_token(user_id="admin")
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        domain = get_doc_or_none(Domain, name=domain_name)
        if domain is None:
            domain = Domain(name=domain_name)
            domain.save()
            logger.info("Domain created: {}", domain_name)
        else:
            logger.info("Domain exists: {}", domain_name)

        resp = await client.get(
            f"{API_BASE}/domains/{domain_name}/init",
            headers=headers,
            timeout=30,
        )
        if resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        logger.info("Domain initialized: {}", domain_name)

        with open(EXAMPLES_DATA_FOLDER / "center_hall.ttl", "rb") as fp:
            files = {
                "file": ("center_hall.ttl", fp, "application/octet-stream"),
            }
            resp = await client.post(
                f"{API_BASE}/domains/{domain_name}/upload",
                headers=headers,
                files=files,
                follow_redirects=False,
            )
            if resp.status_code != 200:
                logger.error("{} {}", resp, resp.request)
                exit(-1)
            await ensure_graphdb_upload(domain_name, "center_hall.ttl")
            logger.info("Domain brick schema initialized: {}", domain_name)


async def create_domain_app(domain_name, app_name):
    user_jwt = create_jwt_token(user_id="admin", domain=domain_name)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        resp = await client.post(
            f"{API_BASE}/domains/{domain_name}/apps/{app_name}",
            headers=headers,
        )
        if resp.status_code == 409:
            logger.info("Domain app exists: {} {}", domain_name, app_name)
        elif resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            logger.info("Domain app created: {}", domain_name, app_name)


async def create_domain_user(user_id, domain_name):
    user_jwt = create_jwt_token(user_id="admin", domain=domain_name)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        resp = await client.post(
            f"{API_BASE}/domains/{domain_name}/users/{user_id}",
            headers=headers,
            follow_redirects=True,
        )
        if resp.status_code == 409:
            logger.info("Domain user exists: {} {}", domain_name, user_id)
        elif resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            pass
            # logger.info("Domain user created: {} {}", domain_name, user_id)


async def create_domain_user_app(user_id, domain_name, app_name, room):
    user_jwt = create_jwt_token(user_id=user_id, domain=domain_name, app_name=app_name)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        resp = await client.post(
            f"{API_BASE}/user/domains/{domain_name}/apps/{app_name}",
            headers=headers,
            follow_redirects=True,
        )
        if resp.status_code == 409:
            logger.info(
                "Domain user app exists: {} {} {}", domain_name, user_id, app_name
            )
        elif resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            pass
            # logger.info(
            #     "Domain user app created: {} {} {}", domain_name, user_id, app_name
            # )

        data = {"arguments": {"room": room}}
        resp = await client.post(
            f"{API_BASE}/user/domains/{domain_name}/apps/{app_name}/init",
            headers=headers,
            json=data,
            follow_redirects=True,
        )
        if resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            pass
            # logger.info(
            #     "Domain user app set room: {} {} {} {}",
            #     domain_name,
            #     user_id,
            #     app_name,
            #     room,
            # )


async def create_permission_profile(user_id, domain_name, app_name, read, write):
    user_jwt = create_jwt_token(user_id="admin", domain=domain_name, app_name=app_name)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        data = {"read": read, "write": write}
        resp = await client.post(
            f"{API_BASE}/profiles",
            headers=headers,
            json=data,
            follow_redirects=True,
        )
        if resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            logger.info("Permission profile created: {}", user_id)
            return resp.json()["id"]


async def create_domain_user_profile(user_id, domain_name, app_name, profile, room):
    user_jwt = create_jwt_token(user_id="admin", domain=domain_name, app_name=app_name)
    headers = {"Authorization": "Bearer " + user_jwt}
    async with httpx.AsyncClient(headers=headers, base_url=API_BASE) as client:
        data = {"profile": profile, "arguments": {"room": room}}
        resp = await client.post(
            f"{API_BASE}/domains/{domain_name}/users/{user_id}/profiles",
            headers=headers,
            json=data,
            follow_redirects=True,
        )
        if resp.status_code != 200:
            logger.error("{} {}", resp, resp.request)
            exit(-1)
        else:
            pass
            # logger.info(
            # "Domain user profile created: {} {} {}", domain_name, user_id, room
            # )


profiles = []


async def init_user(i):
    user_id = f"user{i}"
    create_user(user_id)
    await create_domain_user(user_id, DOMAIN_NAME)
    room = np.random.choice(ROOMS, 1)[0]
    await create_domain_user_app(user_id, DOMAIN_NAME, APP_NAME, room)
    rooms = np.random.choice(ROOMS, i % MAX_PROFILES + 1)
    for j, room in enumerate(rooms):
        await create_domain_user_profile(
            user_id, DOMAIN_NAME, APP_NAME, profiles[j], room
        )


async def init_benchmark():
    logger.info("---------- Initialize benchmark ---------- ")
    reset_mongodb()
    create_user("admin", is_admin=True)
    await create_app(APP_NAME)
    await create_domain(DOMAIN_NAME)
    await create_domain_app(DOMAIN_NAME, APP_NAME)
    await create_domain_user("admin", DOMAIN_NAME)
    await create_domain_user_app("admin", DOMAIN_NAME, APP_NAME, ROOMS[0])
    for i in range(MAX_PROFILES):
        profiles.append(
            await create_permission_profile(
                i, DOMAIN_NAME, APP_NAME, query_app_read, query_app_write
            )
        )

    for i in tqdm(range(MAX_USERS)):
        await init_user(i)
    logger.info("---------- Initialize benchmark completed ---------- ")


@click.group()
@click.help_option("--help", "-h")
def cli_group():
    pass


@click.command()
@click.help_option("--help", "-h")
def init():
    asyncio.run(init_benchmark())


@click.command()
@click.option("-i", "--iterations", type=int, default=0)
@click.argument("name", required=True)
@click.help_option("--help", "-h")
def test(iterations, name):
    cache = os.getenv("CACHE") or "false"
    is_cache = cache.lower() == "true"
    if is_cache:
        logger.info("Cache enabled.")
    else:
        logger.info("Cache disabled.")
    tests = {
        "capability": test_1,
        "validator": test_2,
        "resource": test_3,
        "range": test_4,
        "predictor": test_5,
    }
    if name in tests:
        test_func = tests[name]
        if iterations == 0:
            asyncio.run(test_func(warmup=is_cache))
        else:
            asyncio.run(test_func(iterations=iterations, warmup=is_cache))
    else:
        logger.error("Test {} not found!", name)


if __name__ == "__main__":
    cli_group.add_command(init)
    cli_group.add_command(test)
    asyncio.run(cli_group())
