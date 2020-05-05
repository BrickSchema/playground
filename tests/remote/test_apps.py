from urllib.parse import quote_plus
import yaml
import pdb
from pdb import set_trace as bp

from .common import APP_BASE, authorize_headers, BRICK, app_manifest, requests_post
from .data import znt_id


def test_stage_app():
    headers = authorize_headers()
    manifest = yaml.load(open(app_manifest))
    resp = requests_post(APP_BASE + '/', json=manifest, headers=headers)
    assert resp.status_code in [200, 409]
