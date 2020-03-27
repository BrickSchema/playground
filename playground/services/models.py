from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum

from fastapi import Security


app_name_desc = 'An application\'s name'
app_id_desc = 'The identifier of the app'
perm_templates_desc = 'TODO'


class PermissionTemplate(BaseModel):
    queries: List[Dict[str, str]]
    common_variables: List[List[str]]
    target_variables: List[str]
    permission_type: List[str]

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
    description: str = Field(..., description='A description of the app')
    permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)
    callback_url: str = Field(...)
    app_lifetime: int = Field(..., description='The app\'s lifetime in seconds')
    token_lifetime: int = Field(..., description='Individual token\'s lifetime for this app in seconds')


class AppModificationRequest(BaseModel):
    name: str = Field(..., description=app_name_desc)
    description: str = Field(..., description='A description of the app')
    #TODO: Activate the below later.
    #permission_templates: PermissionTemplates = Field(..., description=perm_templates_desc)
    #callback_url: str = Field(...)
    #app_lifetime: int = Field(..., description='The app\'s lifetime in timestamp seconds')
    #token_lifetime: int = Field(..., description='Individual token\'s lifetime for this app in seconds')
