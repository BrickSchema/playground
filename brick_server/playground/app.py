import os

from fastapi import FastAPI
from fastapi_rest_framework import config
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from brick_server.minimal.app import initialization
from brick_server.playground.config import FastAPIConfig

settings = config.init_settings(FastAPIConfig)
print(settings.dict())

# from brick_server import app as brick_server_app
from brick_server.minimal.dependencies import update_dependency_supplier
from brick_server.minimal.services.actuation import actuation_router
from brick_server.minimal.services.data import data_router
from brick_server.minimal.services.entities import entity_router
from brick_server.minimal.services.queries import query_router

from .auth.auth_server import auth_router
from .auth.authorization import auth_logic
from .services.admins import admin_router
from .services.apps import app_router
from .services.market_apps import marketapp_router
from .services.users import user_router

# from brick_server.dummy_frontend import dummy_frontend_router
# from brick_server.configs import configs


update_dependency_supplier(auth_logic)
app = FastAPI(title="Brick Server Playground", openapi_url="/docs/openapi.json")


@app.on_event("startup")
async def startup_event() -> None:
    await initialization()


app.include_router(data_router, prefix="/brickapi/v1/data")
app.include_router(entity_router, prefix="/brickapi/v1/entities")
app.include_router(query_router, prefix="/brickapi/v1/rawqueries")
app.include_router(actuation_router, prefix="/brickapi/v1/actuation")

app.secret_key = os.urandom(24)
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))

# httphost = configs['hostname'].replace('https','http')
# httpshost = configs['hostname']

# @app.middleware("http")
# async def change_redirect_to_https(request: Request, call_next):
#     response = await call_next(request)
#     if response.status_code >= 300 and response.status_code < 400 and response.headers.get('location'):
#         response.headers['location'] = response.headers['location'].replace(httphost, httpshost)
#
#     return response


app.include_router(app_router, prefix="/brickapi/v1/apps")
app.include_router(marketapp_router, prefix="/brickapi/v1/market_apps")
app.include_router(user_router, prefix="/brickapi/v1/user")
app.include_router(auth_router, prefix="/brickapi/v1/auth")
app.include_router(admin_router, prefix="/brickapi/v1/admin")

app.mount("/brickapi/v1/appstatic", StaticFiles(directory="static"), name="static")
