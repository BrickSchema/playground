from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from brick_server.services.models import Relationships

from fastapi import Security


app_name_desc = 'An application\'s name'
app_desc_desc = 'A description of the app'
app_id_desc = 'The identifier of the app'
perm_templates_desc = 'TODO'
user_id_desc = 'The ID of an user for the request'


class ActivationRequest(BaseModel):
    app_name: str

class ActivatedApps(BaseModel):
    activated_apps: List[str]

class PermissionTemplate(BaseModel):
    queries: List[Dict[str, str]]
    common_variables: List[List[str]]
    target_variables: List[str]
    permission_type: str

PermissionTemplates = Dict[str, PermissionTemplate]


class AppResponse(BaseModel):
    name: str = Field(..., description=app_name_desc)
    description: str = Field(..., description='A description of the app')
    app_id: str = Field(..., description=app_id_desc)
    permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)
    callback_url: str = Field(...)
    app_lifetime: int = Field(..., description='The app\'s lifetime in timestamp seconds')
    token_lifetime: int = Field(..., description='Individual token\'s lifetime for this app in seconds')
    is_approved: bool = Field(...)

AppsResponse = List[AppResponse]

class AppManifest(BaseModel):
    name: str = Field(..., description=app_name_desc)
    description: str = Field(..., description=app_desc_desc)
    permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)
    callback_url: str = Field(...)
    token_lifetime: int = Field(..., description='Individual token\'s lifetime for this app in seconds')


class AppModificationRequest(BaseModel):
    name: str = Field(..., description=app_name_desc)
    description: str = Field(..., description='A description of the app')
    #TODO: Activate the below later.
    #permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)
    #callback_url: str = Field(...)
    #app_lifetime: int = Field(..., description='The app\'s lifetime in timestamp seconds')
    #token_lifetime: int = Field(..., description='Individual token\'s lifetime for this app in seconds')

class AppStageRequest(BaseModel):
    app_name: str = Field(..., description=app_name_desc)
    app_lifetime: int = Field(..., description='The lifetime of the app in seconds')

class UserResponse(BaseModel):
    name: str = Field(...)
    user_id: str = Field(...)
    email: str = Field(...)
    is_admin: bool = Field(...)
    is_approved: bool = Field(...)
    registration_time: Optional[datetime] = None
    activated_apps: List[str]

class MarketAppResponse(BaseModel):
    name: str = Field(..., description=app_name_desc)
    description: str = Field(..., description=app_desc_desc)
    permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)

class AppApprovalRequest(BaseModel):
    app_name: str = Field(..., description=app_name_desc)

class PendingApprovalsResponse(BaseModel):
    admins: List[str]

class UserRelationshipsRequest(Relationships):
    graph: str = Field(None)

