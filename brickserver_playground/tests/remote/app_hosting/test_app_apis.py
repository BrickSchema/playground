import time

import pytest
import yaml

from ..common import (
    APP_BASE,
    AUTH_BASE,
    app_manifest,
    authorize_headers,
    create_jwt_token,
    requests_get,
)

app1_token = create_jwt_token(app_name="app1").decode("utf-8")


@pytest.mark.order(1000)
def test_login_per_app_internal():
    headers = authorize_headers()
    manifest = yaml.full_load(open(app_manifest))
    params = {"external": False}
    resp = requests_get(
        AUTH_BASE + "/app_login/" + manifest["name"],
        headers=headers,
        params=params,
        allow_redirects=False,
    )
    time.sleep(5)
    assert resp.status_code in [200, 409]


@pytest.mark.order(1001)
def test_get_app_api():
    api_url = "/api/get_average_power"
    url = APP_BASE + "/app1/api/" + api_url
    params = {
        "test": "TEST",
    }
    resp = requests_get(url, params=params, cookies={"app_token": app1_token})
    assert resp.status_code == 200


KILL_CMD = "/exit"


@pytest.mark.order(1002)
def test_kill_app_api():
    url = APP_BASE + "/app1/api" + KILL_CMD
    resp = requests_get(url, cookies={"app_token": app1_token})
    assert resp.status_code == 200
