from fastapi import FastAPI
import os

from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

#from brick_server import app as brick_server_app
from brick_server.dependencies  import update_dependency_supplier
from brick_server.services.entities import entity_router
from brick_server.services.data import data_router
from brick_server.services.queries import query_router
from brick_server.services.actuation import actuation_router
from brick_server.dummy_frontend import dummy_frontend_router


from .auth.authorization import evaluate_app_user
from .auth.auth_server import auth_router
from .services.apps import app_router
from .services.market_apps import marketapp_router
from .services.users import user_router as user_app_router

update_dependency_supplier('auth_logic', evaluate_app_user)

#app = brick_server_app

app = FastAPI(__name__, title='Brick Server', openapi_url='/docs/openapi.json')
app.include_router(data_router, prefix='/brickapi/v1/data')
app.include_router(entity_router, prefix='/brickapi/v1/entities')
app.include_router(query_router, prefix='/brickapi/v1/rawqueries')
app.include_router(actuation_router, prefix='/brickapi/v1/actuation')

app.secret_key = os.urandom(24)
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))


app.include_router(app_router, prefix='/brickapi/v1/apps')
app.include_router(marketapp_router, prefix='/brickapi/v1/market_apps')
app.include_router(user_app_router, prefix='/brickapi/v1/user')
app.include_router(auth_router, prefix='/auth')

app.mount("/brickapi/v1/appstatic", StaticFiles(directory="static"), name="static")
