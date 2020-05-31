from pdb import set_trace as bp
import os
import time
import requests
from redis import StrictRedis
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
from starlette.responses import HTMLResponse, FileResponse, Response

from brick_server.exceptions import MultipleObjectsFoundError, AlreadyExistsError, DoesNotExistError, NotAuthorizedError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.auth.authorization import authorized_frontend
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest, AppStageRequest
from .models import app_name_desc
from ..models import StagedApp, User, MarketApp # TODO: Change naming conventino for mongodb models
from ..app_management.app_management import get_cname, stop_container
from ..dbs import get_app_management_redis_db


app_router = InferringRouter('apps')

def get_app_admins(*args, **kwargs):
    app_name = kwargs['app_name']
    app_doc = get_doc(StagedApp, name=app_name)
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
        app_doc = get_doc(StagedApp, name=app_name)
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
        app_doc = get_doc(StagedApp, name=app_name)
        app_doc.delete()
        return IsSuccess()

    @app_router.post('/{app_name}',
                     status_code=200,
                     description='modify metadata of the app.',
                     )
    @authorized
    def modify_staged_app(self,
                  app_name: str = Path(..., description=app_name_desc),
                  app_modification: AppResponse = Body(...),
                  token: HTTPAuthorizationCredentials = jwt_security_scheme,
                  ):
        # TODO: Is it ever used?
        updates = {'set__' + k: v for k, v in app_modeification.dict().items()}
        app_doc = get_doc(StagedApp, name=app_name)
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
        for app_doc in StagedApp.objects():
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
    async def stage_app(self,
                   stage_request: AppStageRequest = Body(...),
                   token: HTTPAuthorizationCredentials = jwt_security_scheme,
                   ):
        jwt_payload = parse_jwt_token(token.credentials)
        #TODO: Check is_admin

        app_name = stage_request.app_name
        existing_apps = StagedApp.objects(name=app_name)
        if existing_apps:
            raise AlreadyExistsError(StagedApp, app_name)
        market_app = get_doc(MarketApp, name=app_name)
        app = StagedApp(
            name=market_app.name,
            app_id = market_app.name,
            description = market_app.description,
            app_expires_at = time.time() + stage_request.app_lifetime,
            token_lifetime = market_app.token_lifetime,
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
        app = get_doc(StagedApp, name=app_name)
        if app not in user.activated_apps:
            raise NotAuthorizedError(detail='The user have not installed the app')

        filepath = 'static/' + app_name + '/' + path
        if not os.path.exists(filepath):
            raise DoesNotExistError('File', filepath)
        resp = FileResponse(filepath)
        # TODO: Update app_token if it is about to expire.
        resp.set_cookie(key='app_token', value=app_token)
        return resp

EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']

@cbv(app_router)
class AppApi():
    caddr_db: StrictRedis = Depends(get_app_management_redis_db)

    @app_router.get('/{app_name}/api/{path:path}',
                     status_code=200,
                     description='List all apps . (Not implemented yet)',
                     )
    async def app_api_get(self,
            request: Request,
            path: str = Path(..., description='TODO'),
            app_name: str=Path(..., description='TODO'),
            app_token: str = Cookie(...), # TODO: Eanble this
            ):
        token_payload = parse_jwt_token(app_token)
        assert token_payload['app_id'] == app_name
        user_id = token_payload["user_id"]
        user = get_doc(User, user_id=user_id)

        cname = get_cname(app_name, user_id)
        container_ip = self.caddr_db.get(cname)
        if path == "exit": #TODO: find a better naming convention.
            print("stopping " + cname)
            stop_container(cname)
            return IsSuccess()

        if container_ip:
            container_url = 'http://' + container_ip + ':5000/' # TODO: Configure the port
        else:
            raise DoesNotExistError('Container', cname)

        dest = container_url + '/' + path
        request_data = await request.body()
        api_resp = requests.request(
            method=request.method,
            url=dest,
            #url=request.url.replace(request.host_url, container_url).replace(request.path, '/'+path),
            headers={key: value for key, value in request.headers.items() if key != 'Host'},
            data=request_data,
            cookies=request.cookies,
            allow_redirects=False,
        )
        headers = {name: value for name, value in api_resp.raw.headers.items()
                   if name.lower() not in EXCLUDED_HEADERS}

        resp = Response(api_resp.content,
                        status_code=api_resp.status_code,
                        headers=headers,
                        )
        return resp

