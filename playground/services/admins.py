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
from brick_server.auth.authorization import authorized_frontend, authorized_admin
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.configs import configs
from brick_server.models import get_doc
#from ..dependencies import get_brick_db, dependency_supplier

from .models import AppResponse, AppManifest, ActivationRequest, ActivatedApps, UserResponse, AppApprovalRequest, PendingApprovalsResponse
from .models import app_name_desc, user_id_desc
from ..models import App, User # TODO: Change naming conventino for mongodb models


admin_router = InferringRouter('admins')

@cbv(admin_router)
class AppApproval:
    @admin_router.post('/app_approval',
                       status_code=200,
                       description='Get User info',
                       response_model=IsSuccess,
                       tags=['Users'],
                       )
    @authorized_admin
    async def approve_app(self,
                          approval_request: AppApprovalRequest,
                          token: HTTPAuthorizationCredentials = jwt_security_scheme,
                          ) -> IsSuccess:
        #TODO Implement the logic
        return IsSuccess()

    @admin_router.get('/app_approval/{app_name}',
                      status_code=200,
                      description='Get User info',
                      response_model=PendingApprovalsResponse,
                      tags=['Users'],
                      )
    async def check_app_approval(self,
                                 app_name: str = Path(..., description=app_name_desc),
                                 ):
        #TODO: Implement Logic
        return PendingApprovalsResponse(admins=[])



