from urllib.parse import quote_plus
import yaml
import pdb
from pdb import set_trace as bp

from .common import MARKETAPP_BASE, authorize_headers, BRICK, requests_get
from .data import znt_id


def test_get_market_apps():
    headers = authorize_headers()
    resp = requests_get(MARKETAPP_BASE, headers=headers)
    assert resp.status_code == 200
