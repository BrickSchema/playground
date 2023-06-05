import pytest
import yaml

from .common import (
    USER_APP_BASE,
    app_manifest,
    authorize_headers,
    requests_delete,
    requests_get,
    requests_post,
)


@pytest.mark.order(700)
def test_deactivate_all_apps():
    headers = authorize_headers()
    resp = requests_delete(USER_APP_BASE, headers=headers)
    assert resp.status_code == 200


@pytest.mark.order(701)
def test_activate_new_app():
    headers = authorize_headers()
    manifest = yaml.full_load(open(app_manifest))
    resp = requests_post(
        USER_APP_BASE, json={"app_name": manifest["name"]}, headers=headers
    )
    assert resp.status_code in [200, 409]


@pytest.mark.order(702)
def test_get_activated_user_apps():
    headers = authorize_headers()
    manifest = yaml.full_load(open(app_manifest))
    resp = requests_get(USER_APP_BASE, headers=headers)
    assert resp.status_code in [200]
    assert manifest["name"] in resp.json()["activated_apps"]


# def test_login_per_app_external():
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
