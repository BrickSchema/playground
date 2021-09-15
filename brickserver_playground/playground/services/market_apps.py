from pdb import set_trace as bp
import time
from copy import deepcopy
from uuid import uuid4
def gen_uuid():
    return str(uuid4())
from io import StringIO
import asyncio
from typing import ByteString, Any, Dict, Callable
from collections import defaultdict

import arrow
import rdflib
from rdflib import RDF, URIRef
from fastapi_utils.cbv import cbv
from fastapi import Depends, Header, HTTPException, Body, Query, Path
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from brick_server.exceptions import MultipleObjectsFoundError
from brick_server.models import get_docs, get_doc
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.auth.authorization import authorized_frontend, authenticated
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest, MarketAppResponse
from .models import app_name_desc
from ..models import MarketApp # TODO: Change naming conventino for mongodb models


marketapp_router = InferringRouter(prefix='/market_apps')

@cbv(marketapp_router)
class MarketAppsRoute():

    @marketapp_router.get('/',
                          status_code=200,
                          description='List all apps . (Not implemented yet)',
                          )
    @authenticated
    async def get_market_apps(self,
                              token: HTTPAuthorizationCredentials = jwt_security_scheme,
                              ):
        #TODO: Check if admin
        market_apps = get_docs(MarketApp)
        res = {'market_apps': [app.name for app in market_apps]}
        return res

    @marketapp_router.get('/{app_name}',
                          status_code=200,
                          description='Get the detail of an app',
                          )
    @authenticated
    async def get_market_app(self,
                       app_name: str = Path(..., description='The name of the app'),
                       token: HTTPAuthorizationCredentials = jwt_security_scheme,
                       ):
        app = get_doc(MarketApp, name=app_name)
        return MarketAppResponse(
            name=app.name,
            description=app.description,
            permission_templates=app.permission_templates
        )

