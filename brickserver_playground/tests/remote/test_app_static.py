import os

import pytest

from .common import APP_BASE, create_jwt_token, get_session, requests_get


@pytest.mark.order(1100)
def test_get_app_static():
    url = APP_BASE + "/app1/static/child/me.html"
    dummy_token = "DUMMY_TOKEN"
    resp = requests_get(url, cookies={"app_token": dummy_token})
    assert resp.status_code == 400
    resp = requests_get(url, cookies={"app_token": os.environ["JWT_TOKEN"]})
    assert resp.status_code == 401

    app1_token = create_jwt_token(app_name="app1").decode("utf-8")

    # Put the token into the URL first. You will get this token from LoginPerApp api first.
    with get_session() as session:
        url = APP_BASE + "/app1/static/index.html"
        authorized_url = url + "?app_token_query=" + app1_token
        resp = session.get(authorized_url)
        # print(resp.text)
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]
        assert session.cookies["app_token"]
        resp = session.get(url)
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]

        url = APP_BASE + "/app1/static/child/me.html"
        authorized_url = url + "?app_token_query=" + app1_token
        resp = session.get(authorized_url)
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]
        assert session.cookies["app_token"]
        resp = session.get(url)
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]
        url = APP_BASE + "/app1/static/child/me.html"

    # Token is already in the cookie
    with get_session() as session:
        resp = session.get(url, cookies={"app_token": app1_token})
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]
        resp = session.get(url)
        assert resp.status_code == 200
        assert resp.text
        assert resp.cookies["app_token"]
