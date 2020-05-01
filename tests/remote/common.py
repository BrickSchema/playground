import os
from copy import deepcopy
from rdflib import Namespace
import pytest

BRICK_VERSION = '1.0.3'
BRICK = Namespace(f'https://brickschema.org/schema/{BRICK_VERSION}/Brick#')

#HOSTNAME = 'https://bd-datas2.ucsd.edu'
#HOSTNAME = 'https://bd-datas2.ucsd.edu'
HOSTNAME = 'https://bd-datas3.ucsd.edu:8000'
#HOSTNAME = ''
API_BASE = HOSTNAME + '/brickapi/v1'
ENTITY_BASE = API_BASE + '/entities'
QUERY_BASE = API_BASE + '/rawqueries'
DATA_BASE = API_BASE + '/data'
ACTUATION_BASE = API_BASE + '/actuation'
APP_BASE = API_BASE + '/apps'
MARKETAPP_BASE = API_BASE + '/market_apps'
USER_APP_BASE = API_BASE + '/user_apps'
AUTH_BASE = HOSTNAME + '/auth'
APP_STATIC_BASE = API_BASE + '/appstatic'

default_headers = {
    "Authorization": "Bearer " + os.environ['JWT_TOKEN']
}

app_manifest = 'examples/data/app_manifests/app1.yaml'


def authorize_headers(headers={}):
    headers.update(default_headers)
    return headers
