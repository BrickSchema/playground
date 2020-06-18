from urllib.parse import quote_plus
import pytest
import yaml
import pdb
from pdb import set_trace as bp

from .common import APP_BASE, authorize_headers, BRICK, app_manifest, requests_post, requests_get
from .data import znt_id


@pytest.mark.run(order=500)
def test_stage_bacnet_driver():
    headers = authorize_headers()
    body = {
        'app_name': 'bacnet_driver',
        'app_lifetime': 15552000, # 6 months
    }
    resp = requests_post(APP_BASE + '/', json=body, headers=headers)
    assert resp.status_code in [200, 409]

@pytest.mark.run(order=501)
def test_stage_app1():
    headers = authorize_headers()
    body = {
        'app_name': 'app1',
        'app_lifetime': 15552000, # 6 months
    }
    resp = requests_post(APP_BASE + '/', json=body, headers=headers)
    assert resp.status_code in [200, 409]

@pytest.mark.run(order=502)
def test_stage_genie():
    headers = authorize_headers()
    body = {
        'app_name': 'genie',
        'app_lifetime': 15552000, # 6 months
    }
    resp = requests_post(APP_BASE + '/', json=body, headers=headers)
    assert resp.status_code in [200, 409]


@pytest.mark.run(order=504)
def test_get_staged_apps():
    headers = authorize_headers()
    resp = requests_get(APP_BASE + '/', headers=headers)
    bp()
    assert resp.status_code in [200, 409]
