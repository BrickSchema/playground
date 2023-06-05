import pytest

from .common import MARKETAPP_BASE, authorize_headers, requests_get


@pytest.mark.order(200)
def test_get_market_apps():
    headers = authorize_headers()
    resp = requests_get(MARKETAPP_BASE, headers=headers)
    assert resp.status_code == 200


@pytest.mark.order(201)
def test_get_market_app():
    headers = authorize_headers()
    resp = requests_get(MARKETAPP_BASE + "/bacnet_driver", headers=headers)
    assert resp.status_code == 200
