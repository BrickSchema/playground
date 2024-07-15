from uuid import uuid4


def gen_uuid():
    return str(uuid4())


from brick_server.auth.authorization import authenticated
from brick_server.models import get_doc, get_docs
from brick_server.services.models import jwt_security_scheme
from fastapi import Path
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from ..models import MarketApp  # TODO: Change naming conventino for mongodb models
from .models import MarketAppResponse

# from ..dependencies import get_brick_db, dependency_supplier


marketapp_router = InferringRouter(prefix="/market_apps")


@cbv(marketapp_router)
class MarketAppsRoute:
    @marketapp_router.get(
        "/",
        status_code=200,
        description="List all apps . (Not implemented yet)",
    )
    @authenticated
    async def get_market_apps(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        # TODO: Check if admin
        market_apps = get_docs(MarketApp)
        res = {"market_apps": [app.name for app in market_apps]}
        return res

    @marketapp_router.get(
        "/{app_name}",
        status_code=200,
        description="Get the detail of an app",
    )
    @authenticated
    async def get_market_app(
        self,
        app_name: str = Path(..., description="The name of the app"),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        app = get_doc(MarketApp, name=app_name)
        return MarketAppResponse(
            name=app.name,
            description=app.description,
            permission_templates=app.permission_templates,
        )
