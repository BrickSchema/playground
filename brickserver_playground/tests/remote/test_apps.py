import pytest

from .common import APP_BASE, authorize_headers, requests_get, requests_post


@pytest.mark.order(500)
def test_stage_bacnet_driver():
    headers = authorize_headers()
    body = {
        "app_name": "bacnet_driver",
        "app_lifetime": 15552000,  # 6 months
    }
    resp = requests_post(APP_BASE + "/", json=body, headers=headers)
    assert resp.status_code in [200, 409]


@pytest.mark.order(501)
def test_stage_app1():
    headers = authorize_headers()
    body = {
        "app_name": "app1",
        "app_lifetime": 15552000,  # 6 months
    }
    resp = requests_post(APP_BASE + "/", json=body, headers=headers)
    assert resp.status_code in [200, 409]


@pytest.mark.order(502)
def test_stage_genie():
    headers = authorize_headers()
    body = {
        "app_name": "genie",
        "app_lifetime": 15552000,  # 6 months
    }
    resp = requests_post(APP_BASE + "/", json=body, headers=headers)
    assert resp.status_code in [200, 409]


# @pytest.mark.order(503)
# def test_destage_app1():
#     headers = authorize_headers()
#     resp = requests_delete(APP_BASE + '/app1', headers=headers)
#     assert resp.status_code == 200


@pytest.mark.order(504)
def test_get_staged_apps():
    headers = authorize_headers()
    resp = requests_get(APP_BASE + "/", headers=headers)
    assert resp.status_code in [200, 409]
    assert "genie" in [app["name"] for app in resp.json()]
    assert "app1" not in [app["name"] for app in resp.json()]
