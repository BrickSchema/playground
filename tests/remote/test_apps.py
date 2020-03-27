from urllib.parse import quote_plus
import yaml
import pdb
import requests
from pdb import set_trace as bp

from .common import APP_BASE, authorize_headers, BRICK
from .data import znt_id


def test_stage_app():
    headers = authorize_headers()
    manifest = yaml.load(open('examples/data/app_manifests/sample_app.yaml'))
    resp = requests.post(APP_BASE, json=manifest, headers=headers)
    bp()
    assert resp.status_code == 200
    assert resp.json()['type'].split('#')[-1] == 'Zone_Air_Temperature_Sensor'
