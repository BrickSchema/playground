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
from brick_server.services.models import relationships_desc
from brick_server.auth.authorization import authorized_frontend, authenticated
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
from brick_server.dependencies import get_brick_db
from brick_server.dbs import BrickSparqlAsync

from .models import AppResponse, AppManifest, ActivationRequest, ActivatedApps, UserResponse, UserRelationshipsRequest
from .models import app_name_desc, user_id_desc
from ..models import StagedApp, User


user_router = InferringRouter(prefix='/users')

@cbv(user_router)
class UserRelationResource:
    brick_db: BrickSparqlAsync = Depends(get_brick_db)

    @user_router.post('/relationship',
                      description='Update a user\'s relationship',
                      response_model=IsSuccess,
                      tags=['Users'],
                      )
    @authenticated
    async def add_user_relation(self,
                          relation_req: UserRelationshipsRequest = Body(..., description='TODO'),
                          token:HTTPAuthorizationCredentials = jwt_security_scheme,
                          ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        #TODO: Interpret the graph
        for p, o in relation_req.relationships:
        # TODO: Verify p and o are valid
            await self.brick_db.add_triple(URIRef(user.user_id), p, o)
        return IsSuccess()


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

        return resp

    @user_router.delete('/apps',
                        status_code=200,
                        description='Deactivate all the apps for this user (for development)',
                        response_model=IsSuccess,
                        tags=['Users'],
                        )
    def deactivate_all_apps(self,
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
    def actviate_app(self,
                     activation_req: ActivationRequest = Body(...),
                     token: HTTPAuthorizationCredentials = jwt_security_scheme,
                     ) -> IsSuccess:
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        app_name = activation_req.app_name
        app = get_doc(StagedApp, name=app_name)
        if app in user.activated_apps:
            raise AlreadyExistsError(StagedApp, app_name)
        app_id = app.app_id
        user.activated_apps.append(app)
        user.save()
        return IsSuccess(reason='Already activated')
