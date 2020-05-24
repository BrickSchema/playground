from urllib.parse import quote_plus
import yaml
from pdb import set_trace as bp

from .common import USER_APP_BASE, authorize_headers, BRICK, AUTH_BASE, app_manifest, requests_delete, requests_post, requests_get, APP_BASE
from .data import znt_id


def test_deactivate_all_apps():
    headers = authorize_headers()
    resp = requests_delete(USER_APP_BASE, headers=headers)
    assert resp.status_code == 200

def test_activate_new_app():
    headers = authorize_headers()
    manifest = yaml.full_load(open(app_manifest))
    resp = requests_post(USER_APP_BASE, json={'app_name': manifest['name']}, headers=headers)
    assert resp.status_code in [200, 409]


def test_get_activated_user_apps():
    headers = authorize_headers()
    manifest = yaml.full_load(open(app_manifest))
    resp = requests_get(USER_APP_BASE, headers=headers)
    assert resp.status_code in [200]
    assert manifest['name'] in resp.json()['activated_apps']

#def test_login_per_app_external():
#    headers = authorize_headers()
#    manifest = yaml.full_load(open(app_manifest))
#    params = {
#        'external': True
#    }
#    resp = requests_get(AUTH_BASE + '/app_login/' + manifest['name'],
#                        headers=headers,
#                        params=params,
#                        allow_redirects=False,
#                        )
#    assert resp.status_code == 307
#    assert resp.cookies['app_token']


def test_login_per_app_internal():
    headers = authorize_headers()
    manifest = yaml.load(open(app_manifest))
    params = {
        'external': False
    }
    resp = requests_get(AUTH_BASE + '/app_login/' + manifest['name'],
                        headers=headers,
                        params=params,
                        allow_redirects=False,
                        )
    assert resp.status_code in [200, 409]
