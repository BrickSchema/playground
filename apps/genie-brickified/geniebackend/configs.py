import os
import json
from dotenv import load_dotenv

load_dotenv()
config_path = os.environ.get('GETNIE_BACKEND_CONFIG', None)
if not config_path:
    config_path = './configs/backend_configs.json'
config = json.load(open(config_path, 'r'))
config["api_token"] = os.environ.get('BRICK_SERVER_API_TOKEN')
# config["brickapi"]["API_URL"] = os.environ.get('BRICK_SERVER_API_URL', None) or config["brickapi"]["API_URL"]
assert config["api_token"]
