from urllib.parse import quote_plus
import yaml
import pdb
import requests
from pdb import set_trace as bp

from .common import APP_STATIC_BASE, authorize_headers, BRICK, app_manifest
from .common import requests_get
from .data import znt_id


def test_stage_app():
    headers = authorize_headers() #TODO This should use a specific app token.
    manifest = yaml.full_load(open(app_manifest))
    app_name = manifest['name']
    resp = requests_get(APP_STATIC_BASE + '/' + app_name + '/index.html',
                         json=manifest,
                         headers=headers,
                         )
    #resp = requests.post(APP_BASE + '/', json=manifest, headers=headers)
    assert resp.status_code in [200, 409]
