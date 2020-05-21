from pdb import set_trace as bp
import os
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
from starlette.responses import HTMLResponse, FileResponse

from brick_server.exceptions import MultipleObjectsFoundError, AlreadyExistsError, DoesNotExistError, NotAuthorizedError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.auth.authorization import authorized_frontend
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest
from .models import app_name_desc
from ..models import App, User # TODO: Change naming conventino for mongodb models


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
    @app_router.get('/{app_name}/static/{path:path}',
                    status_code=200,
                    )
    def get_static(self,
                   app_name: str=Path(..., description='TODO'),
                   path: str = Path(..., description='TODO'),
                   app_token: str = Cookie(None),
                   app_token_query: str = Query(None),
                   ):
        #TODO: parse paths andread and return the right HTMLResponse
        path_splits = [item for item in os.path.split(path) if item]
        if not app_token and not app_token_query:
            raise HTTPException(status_code=400,
                                detail='An `app_token` should be given either in cookie or as a query parameter.',
                                )
        if not app_token and app_token_query:
            app_token = app_token_query
        payload = parse_jwt_token(app_token) #TODO: Change app_id to app_name later
        target_app = payload['app_id']
        if app_name != target_app:
            raise NotAuthorizedError(detail='The given app token is not for the target app')
        user = get_doc(User, user_id=payload['user_id'])
        app = get_doc(App, name=app_name)
        if app not in user.activated_apps:
            raise NotAuthorizedError(detail='The user have not installed the app')

        filepath = 'static/' + app_name + '/' + path
        if not os.path.exists(filepath):
            raise DoesNotExistError('File', filepath)
        resp = FileResponse(filepath)
        # TODO: Update app_token if it is about to expire.
        resp.set_cookie(key='app_token', value=app_token)
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
