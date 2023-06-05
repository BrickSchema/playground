import os
import sys

sys.path.append("./brick-server-minimal")
from playground import app

os.environ["BRICK_CONFIGFILE"] = "./configs/configs.json"
from brick_server.auth.authorization import *
from brick_server.configs import configs
from starlette.middleware.cors import CORSMiddleware

frontend = configs["frontend"].get("hostname", configs["hostname"])

origins = [frontend]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# update_dependency_supplier('auth_logic', check_admin2)
