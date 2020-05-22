import os
from contextlib import contextmanager
import json
import time
import sys
import jwt
import requests
from copy import deepcopy
from rdflib import Namespace
import pytest

sys.path.append("./brick-server-minimal")
configs = json.load(open('./configs/configs.json'))

BRICK_VERSION = '1.0.3'
BRICK = Namespace(f'https://brickschema.org/schema/{BRICK_VERSION}/Brick#')

#HOSTNAME = 'https://bd-datas2.ucsd.edu'
#HOSTNAME = 'https://bd-datas2.ucsd.edu'
HOSTNAME = 'https://bd-testbed.ucsd.edu:8000'
#HOSTNAME = ''
API_BASE = HOSTNAME + '/brickapi/v1'
ENTITY_BASE = API_BASE + '/entities'
QUERY_BASE = API_BASE + '/rawqueries'
DATA_BASE = API_BASE + '/data'
ACTUATION_BASE = API_BASE + '/actuation'
APP_BASE = API_BASE + '/apps'
MARKETAPP_BASE = API_BASE + '/market_apps'
USER_APP_BASE = API_BASE + '/user/apps'
AUTH_BASE = HOSTNAME + '/auth'
APP_STATIC_BASE = API_BASE + '/appstatic'

default_headers = {
    "Authorization": "Bearer " + os.environ['JWT_TOKEN']
}

app_manifest = 'examples/data/app_manifests/app1.yaml'


def authorize_headers(headers={}):
    headers.update(default_headers)
    return headers

def requests_get(*args, **kwargs):
    return requests.get(*args, **kwargs, verify=False)

def requests_post(*args, **kwargs):
    return requests.post(*args, **kwargs, verify=False)

def requests_delete(*args, **kwargs):
    return requests.delete(*args, **kwargs, verify=False)


privkey_path = configs['auth']['jwt'].get('privkey_path', 'configs/jwtRS256.key')
pubkey_path = configs['auth']['jwt'].get('pubkey_path', 'configs/jwtRS256.key.pub')
with open(privkey_path, 'r') as fp:
    _jwt_priv_key = fp.read()
with open(pubkey_path, 'r') as fp:
    _jwt_pub_key = fp.read()

def create_jwt_token(user_id: str = 'admin',
                     app_name: str = None,
                     token_lifetime: int = 3600,
                     ):
    payload = {
        'user_id': user_id,
        'exp': time.time() + token_lifetime, # TODO: Think about the timezone
        'app_id': app_name,
    }
    jwt_token = jwt.encode(payload, _jwt_priv_key, algorithm='RS256')
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
