from urllib.parse import quote_plus
import yaml
from pdb import set_trace as bp

from .common import USER_APP_BASE, authorize_headers, BRICK, AUTH_BASE, app_manifest, requests_delete, requests_post, requests_get, APP_BASE, create_jwt_token
from .data import znt_id


app1_token = create_jwt_token(app_name='app1').decode('utf-8')

def test_get_app_api():
    api_url = '/api/get_average_power'
    url = APP_BASE + '/app1/api/' + api_url
    params = {
        'test': 'TEST',
    }
    headers = {
        'testheader': 'HeaderTest',
    }
    resp = requests_get(url, params=params, headers=headers, cookies={'app_token': app1_token})
    assert resp.status_code == 200

KILL_CMD = '/exit'

def test_kill_app_api():
    url = APP_BASE + '/app1/api' + KILL_CMD
    resp = requests_get(url, cookies={'app_token': app1_token})
    assert resp.status_code == 200
