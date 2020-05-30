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

from brick_server.exceptions import MultipleObjectsFoundError, AlreadyExistsError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.auth.authorization import authorized_frontend
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest, ActivationRequest, ActivatedApps, UserResponse
from .models import app_name_desc, user_id_desc
from ..models import App, User # TODO: Change naming conventino for mongodb models


user_router = InferringRouter('users')

@cbv(user_router)
class UserResource:
    @user_router.get('/',
                     status_code=200,
                     description='Get User info',
                     response_model=UserResponse,
                     tags=['Users'],
                     )
    def get_user_info(self,
                      token: HTTPAuthorizationCredentials = jwt_security_scheme,
                      ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        return UserResponse(
            name=user.name,
            user_id=user.user_id,
            email=user.email,
            is_admin=user.is_admin,
            is_approved=user.is_approved,
            activated_apps=[app.name for app in user.activated_apps],
            registration_time=arrow.get(user.registration_time).datetime
        )

@cbv(user_router)
class UserApps:

    @user_router.get('/apps',
                    status_code=200,
                    description='View apps that user activated.',
                    response_model=ActivatedApps,
                    tags=['Users'],
                    )
    def get_activated_apps(self,
                           token: HTTPAuthorizationCredentials = jwt_security_scheme,
                           ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        resp = ActivatedApps(activated_apps=[app.name for app in user.activated_apps])
        bp()

        return resp

    @user_router.delete('/apps',
                        status_code=200,
                        description='Deactivate all the apps for this user (for development)',
                        response_model=IsSuccess,
                        tags=['Users'],
                        )
    #@authorized #TODO: Reimplement the authentication mechanism
    def deactivate_all_apps(self,
                            #user_id: str = Path(..., description=user_id_desc),
                            token: HTTPAuthorizationCredentials = jwt_security_scheme,
                            ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        user.activated_apps = []
        user.save()

        return IsSuccess()

    @user_router.post('/apps',
                    status_code=200,
                    description='Activate an app for the user.',
                    #response_model=AppResponse,
                    tags=['Users'],
                    )
    #@authenticated #TODO: Reimplement the authentication mechanism
    def post(self,
             #user_id: str = Path(..., description=user_id_desc),
             activation_req: ActivationRequest = Body(...),
             token: HTTPAuthorizationCredentials = jwt_security_scheme,
             ) -> IsSuccess:
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        app_name = activation_req.app_name
        app = get_doc(App, name=app_name)
        if app in user.activated_apps:
            raise AlreadyExistsError(App, app_name)
        app_id = app.app_id
        # TODO: I think this is not necessary. Remove below later.
#        for perm_name, perm_template in app.permission_templates.items():
#            #query_template = perm_template['queries']
#            perm_type = perm_template['permission_type']
#            owner_resources = get_owner_resources(perm_template, user_id)
#            for owner in set(owner_resources.keys()):
#                if owner not in app.approvals[perm_name]:
#                    raise exceptions.Unauthorized('{0} is not approved by a resource owner'.format(app_name))
#            for owner, rscs in owner_resources.items():
#                for rsc in rscs:
#                    register_permission(user_id, app, rsc, perm_type)
        user.activated_apps.append(app)
        user.save()
        return IsSuccess(reason='Already activated')
