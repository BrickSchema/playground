import os
import time
from uuid import uuid4

from redis import StrictRedis


def gen_uuid():
    return str(uuid4())


import httpx
from brick_server.minimal.auth.authorization import (
    authorized,
    authorized_frontend,
    jwt_security_scheme,
    parse_jwt_token,
)
from brick_server.minimal.exceptions import (
    AlreadyExistsError,
    DoesNotExistError,
    NotAuthorizedError,
)

# from brick_server.configs import configs
from brick_server.minimal.models import get_doc
from brick_server.minimal.schemas import IsSuccess
from fastapi import Body, Cookie, Depends, HTTPException, Path, Query
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_rest_framework.config import settings
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request
from starlette.responses import FileResponse, Response

from ..app_management.app_management import get_cname, stop_container
from ..dbs import get_app_management_redis_db
from ..models import (  # TODO: Change naming conventino for mongodb models
    MarketApp,
    StagedApp,
    User,
)
from .models import (
    AppResponse,
    AppStageRequest,
    StagedAppResponse,
    StagedAppsResponse,
    app_name_desc,
)

# DEFAULT_ADMIN_ID = configs['app_management']['default_admin']
DEFAULT_ADMIN_ID = settings.default_admin

app_router = InferringRouter()


def get_app_admins(*args, **kwargs):
    app_name = kwargs["app_name"]
    app_doc = get_doc(StagedApp, name=app_name)
    return app_doc.admins


@cbv(app_router)
class AppByName:
    @app_router.get(
        "/{app_name}",
        status_code=200,
        description="Get information about the app",
        response_model=AppResponse,
        tags=["Apps"],
    )
    @authorized  # TODO: Reimplement the authentication mechanism
    def get(
        self,
        app_name: str = Path(..., description=app_name_desc),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        app_doc = get_doc(StagedApp, name=app_name)
        return app_doc

    @app_router.delete(
        "/{app_name}",
        status_code=200,
        description="Delete a app along with its relationships",
    )
    @authorized
    def delete(
        self,
        app_name: str = Path(..., description=app_name_desc),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        app_doc = get_doc(StagedApp, name=app_name)
        app_doc.delete()
        return IsSuccess()

    @app_router.post(
        "/{app_name}",
        status_code=200,
        description="modify metadata of the app.",
    )
    @authorized
    def modify_staged_app(
        self,
        app_name: str = Path(..., description=app_name_desc),
        app_modification: AppResponse = Body(...),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        # TODO: Is it ever used?
        updates = {"set__" + k: v for k, v in app_modification.dict().items()}
        app_doc = get_doc(StagedApp, name=app_name)
        app_doc.update(**updates)
        return "Success", 201


@cbv(app_router)
class Apps:
    @app_router.get(
        "/",
        status_code=200,
        description="List all staged apps.",
        response_model=StagedAppsResponse,
    )
    @authorized_frontend
    async def get(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ) -> StagedAppsResponse:
        return [
            StagedAppResponse(name=app.name, is_approved=not app.pending_approvals)
            for app in StagedApp.objects()
        ]

    @app_router.post(
        "/",
        status_code=200,
        description="Stage an app",
        response_model=IsSuccess,
    )
    @authorized_frontend
    async def stage_app(
        self,
        stage_request: AppStageRequest = Body(...),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        jwt_payload = parse_jwt_token(token.credentials)
        # TODO: Check is_admin

        app_name = stage_request.app_name
        existing_apps = StagedApp.objects(name=app_name)
        if existing_apps:
            raise AlreadyExistsError(StagedApp, app_name)
        market_app = get_doc(MarketApp, name=app_name)
        app = StagedApp(
            name=market_app.name,
            app_id=market_app.name,
            description=market_app.description,
            app_expires_at=time.time() + stage_request.app_lifetime,
            token_lifetime=market_app.token_lifetime,
            installer=jwt_payload["user_id"],
            permission_templates=market_app.permission_templates,
        )
        app.save()

        for perm_name in app.permission_templates.keys():
            # TODO
            # app.approvals[perm_name] = []
            pass
        app.pending_approvals = [
            DEFAULT_ADMIN_ID
        ]  # TODO: This is only for debug. properly implement this later.

        # request_app_approval(app)
        app.save()

        return IsSuccess()


@cbv(app_router)
class AppStatic:
    @app_router.get(
        "/{app_name}/static/{path:path}",
        status_code=200,
    )
    def get_static(
        self,
        request: Request,
        app_name: str = Path(..., description="TODO"),
        path: str = Path(..., description="TODO"),
        app_token: str = Cookie(None),
        app_token_query: str = Query(None),
    ):
        # TODO: parse paths andread and return the right HTMLResponse
        path_splits = [item for item in os.path.split(path) if item]
        if not app_token and not app_token_query:
            raise HTTPException(
                status_code=400,
                detail="An `app_token` should be given either in cookie or as a query parameter.",
            )
        if app_token_query:
            app_token = app_token_query  # prioritize the token over cookies as it's more updated
        payload = parse_jwt_token(app_token)
        target_app = payload["app_id"]  # TODO: Change app_id to app_name later
        if app_name != target_app:
            raise NotAuthorizedError(
                detail="The given app token is not for the target app"
            )
        user = get_doc(User, user_id=payload["user_id"])
        app = get_doc(StagedApp, name=app_name)
        if app not in user.activated_apps:
            raise NotAuthorizedError(detail="The user have not installed the app")

        filepath = "static/" + app_name + "/" + path
        if not os.path.exists(filepath):
            raise DoesNotExistError("File", filepath)
        resp = FileResponse(filepath)
        # TODO: Update app_token if it is about to expire.
        resp.set_cookie(
            key="app_token", value=app_token, path="/brickapi/v1/apps/" + app_name
        )
        # TODO: Find a way to get the path automatically
        return resp


EXCLUDED_HEADERS = [
    "content-encoding",
    "content-length",
    "transfer-encoding",
    "connection",
]


@cbv(app_router)
class AppApi:
    caddr_db: StrictRedis = Depends(get_app_management_redis_db)

    @app_router.api_route(
        "/{app_name}/api/{path:path}",
        methods=["GET", "POST", "DELETE", "PUT", "OPTIONS", "HEAD", "PATCH", "TRACE"],
        status_code=200,
        description="List all apps . (Not implemented yet)",
    )
    async def app_api(
        self,
        request: Request,
        path: str = Path(..., description="TODO"),
        app_name: str = Path(..., description="TODO"),
        app_token: str = Cookie(...),  # TODO: Eanble this
    ):
        token_payload = parse_jwt_token(app_token)
        assert token_payload["app_id"] == app_name
        user_id = token_payload["user_id"]
        user = get_doc(User, user_id=user_id)

        cname = get_cname(app_name, user_id)
        container_ip = self.caddr_db.get(cname)
        if path == "exit":  # TODO: find a better naming convention.
            print("stopping " + cname)
            stop_container(cname)
            return IsSuccess()

        if container_ip:
            container_url = (
                "http://" + container_ip + ":5000/"
            )  # TODO: Configure the port
        else:
            raise DoesNotExistError("Container", cname)

        dest = container_url + path
        request_data = await request.body()
        async with httpx.AsyncClient() as client:
            api_resp = await client.request(
                method=request.method,
                url=dest,
                # url=request.url.replace(request.host_url, container_url).replace(request.path, '/'+path),
                headers={
                    key: value
                    for key, value in request.headers.items()
                    if key != "Host"
                },
                params={key: value for key, value in request.query_params.items()},
                data=request_data,
                allow_redirects=False,
            )
            headers = {
                name: value
                for name, value in api_resp.headers.items()
                if name.lower() not in EXCLUDED_HEADERS
            }

            resp = Response(
                api_resp.content,
                status_code=api_resp.status_code,
                headers=headers,
            )
            return resp
