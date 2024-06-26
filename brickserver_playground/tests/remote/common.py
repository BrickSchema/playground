import json
import os
import sys
import time
from contextlib import contextmanager

import jwt
import requests
from rdflib import Namespace

sys.path.append("./brick-server-minimal")
configs = json.load(open("./configs/configs.json"))

BRICK_VERSION = "1.0.3"
BRICK = Namespace(f"https://brickschema.org/schema/{BRICK_VERSION}/Brick#")

HOSTNAME = os.environ["HOSTNAME"]
ADMIN_ID = os.environ["ADMIN_ID"]
JWT_TOKEN = os.environ["JWT_TOKEN"]
API_BASE = HOSTNAME + "/brickapi/v1"
ENTITY_BASE = API_BASE + "/entities"
QUERY_BASE = API_BASE + "/rawqueries"
DATA_BASE = API_BASE + "/data"
ACTUATION_BASE = API_BASE + "/actuation"
APP_BASE = API_BASE + "/apps"
MARKETAPP_BASE = API_BASE + "/market_apps"
USER_APP_BASE = API_BASE + "/user/apps"
USER_BASE = API_BASE + "/user"
AUTH_BASE = HOSTNAME + "/auth"
APP_STATIC_BASE = API_BASE + "/appstatic"
ADMIN_BASE = API_BASE + "/admin"

default_headers = {"Authorization": "Bearer " + os.environ["JWT_TOKEN"]}

app_manifest = "examples/data/app_manifests/app1.yaml"
genie_manifest = "examples/data/app_manifests/genie.yaml"


def authorize_headers(headers={}):
    headers.update(default_headers)
    return headers


def requests_get(*args, **kwargs):
    return requests.get(*args, **kwargs, verify=False)


def requests_post(*args, **kwargs):
    return requests.post(*args, **kwargs, verify=False)


def requests_put(*args, **kwargs):
    return requests.put(*args, **kwargs, verify=False)


def requests_delete(*args, **kwargs):
    return requests.delete(*args, **kwargs, verify=False)


privkey_path = configs["auth"]["jwt"].get("privkey_path", "configs/jwtRS256.key")
pubkey_path = configs["auth"]["jwt"].get("pubkey_path", "configs/jwtRS256.key.pub")
with open(privkey_path) as fp:
    _jwt_priv_key = fp.read()
with open(pubkey_path) as fp:
    _jwt_pub_key = fp.read()


def create_jwt_token(
    user_id: str = ADMIN_ID,
    app_name: str = None,
    token_lifetime: int = 3600,
):
    payload = {
        "user_id": user_id,
        "exp": time.time() + token_lifetime,  # TODO: Think about the timezone
        "app_id": app_name,
    }
    jwt_token = jwt.encode(payload, _jwt_priv_key, algorithm="RS256")
    return jwt_token


@contextmanager
def get_session():
    sess = requests.Session()
    sess.verify = False
    try:
        yield sess
    finally:
        # Code to release resource, e.g.:
        sess.close()
