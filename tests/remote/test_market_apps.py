from urllib.parse import quote_plus
import yaml
import pdb
import requests
from pdb import set_trace as bp

from .common import MARKETAPP_BASE, authorize_headers, BRICK
from .data import znt_id


def test_get_market_apps():
    headers = authorize_headers()
    resp = requests.get(MARKETAPP_BASE, headers=headers, verify=False)
    assert resp.status_code == 200
