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
from fastapi import Depends, Header, HTTPException, Body, Query, Path, Cookie
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.responses import HTMLResponse

from brick_server.exceptions import MultipleObjectsFoundError, AlreadyExistsError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.auth.authorization import authorized_frontend
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest
from .models import app_name_desc
from ..models import App # TODO: Change naming conventino for mongodb models


app_router = InferringRouter('apps')

def get_app_admins(*args, **kwargs):
    app_name = kwargs['app_name']
    app_doc = get_doc(App, name=app_name)
    return app_doc.admins

@cbv(app_router)
class AppByName:

    @app_router.get('/{app_name}',
                    status_code=200,
                    description='Get information about the app',
                    response_model=AppResponse,
                    tags=['Apps'],
                    )
    @authorized #TODO: Reimplement the authentication mechanism
    def get(self,
            app_name: str = Path(..., description=app_name_desc),
            token: HTTPAuthorizationCredentials = jwt_security_scheme,
            ):
        app_doc = get_doc(App, name=app_name)
        return app_doc


    @app_router.delete('/{app_name}',
                       status_code=200,
                       description='Delete a app along with its relationships',
                       )
    @authorized
    def delete(self,
            app_name: str = Path(..., description=app_name_desc),
            token: HTTPAuthorizationCredentials = jwt_security_scheme,
            ):
        app_doc = get_doc(App, name=app_name)
        app_doc.delete()
        return IsSuccess()

    @app_router.post('/{app_name}',
                     status_code=200,
                     description='modify metadata of the app.',
                     )
    @authorized
    def stage_app(self,
             app_name: str = Path(..., description=app_name_desc),
             app_modification: AppResponse = Body(...),
             token: HTTPAuthorizationCredentials = jwt_security_scheme,
             ):
        # TODO: Is it ever used?
        updates = {'set__' + k: v for k, v in app_modeification.dict().items()}
        app_doc = get_doc(App, name=app_name)
        app_doc.update(**updates)
        return 'Success', 201

@cbv(app_router)
class Apps():

    @app_router.get('/',
                     status_code=200,
                     description='List all apps . (Not implemented yet)',
                     )
    def get(self,
            token: HTTPAuthorizationCredentials = jwt_security_scheme,
            ):
        apps = []
        raise Exception('Not implemented')
        for app_doc in App.objects():
            app = {k: app_doc[k] for k in ['name', 'description']}
            if user_id in app_doc.admins:
                app['callback_url'] = app_doc.callback_url
            apps.append(app)
        res = {'apps': apps}
        return res

    @app_router.post('/',
                     status_code=200,
                     description='Stage an app',
                     response_model=IsSuccess,
                     )
    @authorized_frontend
    async def post(self,
                   manifest: AppManifest,
                   token: HTTPAuthorizationCredentials = jwt_security_scheme,
                   ):
        existing_apps = App.objects(name=manifest.name)
        if existing_apps:
            raise AlreadyExistsError(App, manifest.name)
        jwt_payload = parse_jwt_token(token.credentials)
        app = App(name = manifest.name,
                  app_id = manifest.name,
                  description = manifest.description,
                  callback_url = manifest.callback_url,
                  app_expires_at = time.time() + manifest.app_lifetime,
                  token_lifetime = manifest.token_lifetime,
                  installer = jwt_payload['user_id'],
                  )
        app.save()

        for perm_name in app.permission_templates.keys():
            # TODO
            #app.approvals[perm_name] = []
            #app.pending_approvals[perm_name] = []
            pass
        #request_app_approval(app)
        app.save()

        return IsSuccess()



@cbv(app_router)
class AppStatic():
    @app_router.get('/{app_name}/static/{paths:path}',
                    status_code=200,
                    )
    def get_static(self,
                   app_name: str=Path(..., description='TODO'),
                   paths: str = Path(..., description='TODO'),
                   app_token: str = Cookie(...),
                   ):
        #TODO: parse paths andread and return the right HTMLResponse
        if is_index:
            # TODO: Check if token is inside the cookie.
            #          TODO: Validate Token in the cookie
            # TODO: else:
            #          TODO: Validate Token retrieved from the path
            #          TODO: Set Token in the cookie
            pass
        else:
            #TODO: Validate the Token
            #TODO: Maybe update the token
            pass

        # TODO: If file does not exist, return an error.

        resp = FileResponse('static/' + paths)
        #with open('static/' + paths, 'r') as fp:
        #    if filetype == HTML:
        #        resp = HTMLResponse(fp.read())
        #    else:
                #resp = FileResponse
        return resp


@cbv(app_router)
class AppApi():
    @app_router.get('/{app_name}/api/{paths:path}',
                     status_code=200,
                     description='List all apps . (Not implemented yet)',
                     )
    def get(self,
            request: Request,
            app_name: str=Path(..., description='TODO'),
            #app_token: str = Cookie(...), TODO: Eanble this
            ):
        #TODO: parse request and call the corresponding API
        return res

    @app_router.post('/',
                     status_code=200,
                     description='Stage an app',
                     response_model=IsSuccess,
                     )
    @authorized_frontend
    async def post(self,
                   manifest: AppManifest,
                   token: HTTPAuthorizationCredentials = jwt_security_scheme,
                   ):
        existing_apps = App.objects(name=manifest.name)
        if existing_apps:
            raise AlreadyExistsError(App, manifest.name)
        jwt_payload = parse_jwt_token(token.credentials)
        app = App(name = manifest.name,
                  app_id = manifest.name,
                  description = manifest.description,
                  callback_url = manifest.callback_url,
                  app_expires_at = time.time() + manifest.app_lifetime,
                  token_lifetime = manifest.token_lifetime,
                  installer = jwt_payload['user_id'],
                  )
        app.save()

        for perm_name in app.permission_templates.keys():
            # TODO
            #app.approvals[perm_name] = []
            #app.pending_approvals[perm_name] = []
            pass
        #request_app_approval(app)
        app.save()

        return IsSuccess()
