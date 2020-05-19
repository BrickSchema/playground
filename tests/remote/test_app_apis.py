from urllib.parse import quote_plus
import yaml
from pdb import set_trace as bp

from .common import USER_APP_BASE, authorize_headers, BRICK, AUTH_BASE, app_manifest, requests_delete, requests_post, requests_get, APP_BASE
from .data import znt_id



def test_get_app_api():
    url = APP_BASE + '/app1/api/test'
    params = {
        'test': 'TEST',
    }
    headers = {
        'testheader': 'HeaderTest',
    }
    resp = requests_get(url, params=params, headers=headers)
    bp()
