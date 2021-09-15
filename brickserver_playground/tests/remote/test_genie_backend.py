from urllib.parse import quote_plus
import time
import pytest
import yaml
from pdb import set_trace as bp

from .common import USER_APP_BASE, authorize_headers, AUTH_BASE, genie_manifest, requests_post, requests_get, APP_BASE, create_jwt_token, HOSTNAME, ADMIN_ID, JWT_TOKEN
from .data import znt_id


genie_token = create_jwt_token(app_name='genie').decode('utf-8')


@pytest.mark.order(901)
def test_activate_new_app():
    headers = authorize_headers()
    manifest = yaml.full_load(open(genie_manifest))
    resp = requests_post(USER_APP_BASE, json={'app_name': manifest['name']}, headers=headers)
    assert resp.status_code in [200, 409]


@pytest.mark.order(902)
def test_get_activated_user_apps():
    headers = authorize_headers()
    manifest = yaml.full_load(open(genie_manifest))
    resp = requests_get(USER_APP_BASE, headers=headers)
    assert resp.status_code in [200]
    assert manifest['name'] in resp.json()['activated_apps']


@pytest.mark.order(1000)
def test_login_per_app_internal():
    headers = authorize_headers()
    manifest = yaml.full_load(open(genie_manifest))
    params = {
        'external': False
    }
    resp = requests_get(AUTH_BASE + '/app_login/' + manifest['name'],
                        headers=headers,
                        params=params,
                        allow_redirects=False,
                        )
    time.sleep(5)
    assert resp.status_code in [200, 409]


@pytest.mark.order(1001)
def test_get_app_api():
    api_url = '/api/redirected' # api in genie
    url = APP_BASE + '/genie/api' + api_url
    params = {
        'user_access_token': genie_token
    }
    resp = requests_get(url, params=params, cookies={'app_token': genie_token})
    assert resp.status_code == 200
    assert resp.text == ADMIN_ID


KILL_CMD = '/exit'

@pytest.mark.order(1002)
def test_kill_app_api():
    url = APP_BASE + '/genie/api' + KILL_CMD
    resp = requests_get(url, cookies={'app_token': genie_token})
    assert resp.status_code == 200
