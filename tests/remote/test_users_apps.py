from urllib.parse import quote_plus
import yaml
import pdb
import requests
from pdb import set_trace as bp

from .common import USER_APP, authorize_headers, BRICK, AUTH_BASE
from .data import znt_id


def test_activate_new_app():
    headers = authorize_headers()
    manifest = yaml.load(open('examples/data/app_manifests/sample_app.yaml'))
    resp = requests.post(USER_APP + '/', json={'app_name': manifest['name']}, headers=headers)
    assert resp.status_code in [200, 409]


def test_get_activated_user():
    headers = authorize_headers()
    manifest = yaml.load(open('examples/data/app_manifests/sample_app.yaml'))
    resp = requests.get(USER_APP + '/', headers=headers)
    assert resp.status_code in [200]
    assert manifest['name'] in resp.json()['activated_apps']

def test_login_per_app():
    headers = authorize_headers()
    manifest = yaml.load(open('examples/data/app_manifests/sample_app.yaml'))
    resp = requests.get(AUTH_BASE + '/app_login/' + manifest['name'], headers=headers)
    assert resp.status_code in [200]


