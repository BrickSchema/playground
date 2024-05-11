import asyncio
import json
import pathlib
import subprocess
from shutil import rmtree

import aiofiles
import httpx
from brick_server.minimal.interfaces.cache import clear_cache
from brick_server.minimal.securities.checker import PermissionChecker
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    Form,
    Path,
    UploadFile,
)
from fastapi.concurrency import run_in_threadpool
from fastapi_restful.cbv import cbv
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorGridOut
from patoolib import extract_archive
from redis import StrictRedis
from starlette.requests import Request
from starlette.responses import FileResponse, Response

from brick_server.playground import models, schemas
from brick_server.playground.config.manager import settings
from brick_server.playground.interfaces.app_management import get_container_ip
from brick_server.playground.securities.auth import Authorization
from brick_server.playground.utilities.dependencies import (
    AsyncDatabase,
    get_app_management_redis_db,
    get_mongodb,
    get_path_app,
)
from brick_server.playground.utilities.exceptions import BizError, ErrorCode

# DEFAULT_ADMIN_ID = configs['app_management']['DEFAULT_ADMIN']
# DEFAULT_ADMIN_ID = settings.DEFAULT_ADMIN

router = APIRouter(prefix="/apps", tags=["apps"])


# def get_app_admins(*args, **kwargs):
#     app_name = kwargs["app_name"]
#     app_doc = get_doc(StagedApp, name=app_name)
#     return app_doc.admins


def ensure_safe_path(path, must_exist=False) -> pathlib.Path | None:
    try:
        if must_exist:
            path = pathlib.Path(path).resolve(strict=True)
        else:
            path = pathlib.Path(path).absolute()
        path.relative_to(settings.APP_STATIC_DIR)
        return path
    except Exception as e:
        logger.exception(e)
        return None


@cbv(router)
class AppRoute:

    @router.get("/", description="Get all apps on the site.", name="apps:list")
    async def list_apps(self) -> schemas.StandardListResponse[schemas.AppRead]:
        apps = await models.App.find_all().to_list()
        return schemas.StandardListResponse(
            [schemas.AppRead.model_validate(app.dict()) for app in apps]
        )

    @router.post("/", description="Register an app.", name="apps:registration")
    async def register_app(
        self,
        app_create: schemas.AppCreate = Body(...),
    ) -> schemas.StandardResponse[schemas.AppRead]:
        app = await models.App.find_one(models.App.name == app_create.name)
        if app is not None:
            raise BizError(ErrorCode.AppAlreadyExistsError)
        # profile = models.PermissionProfile(
        #     read=app_create.profile.read,
        #     write=app_create.profile.write,
        # )
        # profile.save()
        app = models.App(
            name=app_create.name,
            description=app_create.description,
            approved=False,
        )
        await app.save()
        return schemas.AppRead.model_validate(app.dict()).to_response()

    @router.get(
        "/{app}",
        description="Get information about an app.",
        name="apps:get",
    )
    async def get_app(
        self,
        app: models.App = Depends(get_path_app),
    ) -> schemas.StandardResponse[schemas.AppReadWithApprovedData]:
        if app.approved_data is not None:
            app.approved_data.permission_profile = (
                await app.approved_data.permission_profile.fetch()
            )
        return schemas.AppReadWithApprovedData.model_validate(app.dict()).to_response()

    @router.delete(
        "/{app}",
        description="Delete an app (site admin).",
        name="apps:delete",
    )
    async def delete_app(
        self,
        app: models.App = Depends(get_path_app),
    ) -> schemas.StandardResponse[schemas.Empty]:
        # TODO: remove all domain_apps, domain_user_apps and containers
        await app.delete()
        return schemas.StandardResponse()

    @staticmethod
    async def replace_file(
        db: AsyncDatabase, app: models.App, file: UploadFile | None, name: str
    ):
        if file is not None:
            submitted_file_id = getattr(app.submitted_data, name)
            approved_file_id = (
                getattr(app.approved_data, name) if app.approved_data else None
            )
            if submitted_file_id != approved_file_id and submitted_file_id is not None:
                try:
                    await db.gridfs_bucket.delete(submitted_file_id)
                    logger.info("Delete unused file: {}", submitted_file_id)
                except Exception as e:
                    logger.info("Delete unused file failed: {}", submitted_file_id)
                    logger.exception(e)

            new_file_id = await db.gridfs_bucket.upload_from_stream(
                filename=file.filename,
                source=file.file,
            )
            setattr(app.submitted_data, name, new_file_id)
            logger.info("Upload file {}: {}", file.filename, new_file_id)

    @router.post(
        "/{app}/submit",
        description="Submit frontend, backend, permission profile and permission model of an app.",
        name="apps:submit_data",
    )
    async def submit_app_data(
        self,
        app: models.App = Depends(get_path_app),
        frontend_file: UploadFile = File(None),
        backend_file: UploadFile = File(None),
        permission_profile_read: str = Form(),
        permission_profile_write: str = Form(),
        permission_profile_arguments: str = Form(),
        permission_model: schemas.PermissionModel = Form(),
        db: AsyncDatabase = Depends(get_mongodb),
    ) -> schemas.StandardResponse[schemas.AppReadWithAllData]:
        permission_profile_arguments = json.loads(permission_profile_arguments)
        if app.submitted_data is None:
            app.submitted_data = models.AppData()
        if app.submitted_data.permission_profile is None:
            permission_profile_model = models.PermissionProfile(
                read=permission_profile_read,
                write=permission_profile_write,
                arguments=permission_profile_arguments,
            )
            await permission_profile_model.save()
            app.submitted_data.permission_profile = permission_profile_model.to_ref()
        else:
            permission_profile_model = (
                await app.submitted_data.permission_profile.fetch()
            )
            permission_profile_model.read = permission_profile_read
            permission_profile_model.write = permission_profile_write
            permission_profile_model.arguments = permission_profile_arguments
            await permission_profile_model.save()

        app.submitted_data.permission_model = permission_model
        await self.replace_file(db, app, frontend_file, "frontend")
        await self.replace_file(db, app, backend_file, "backend")
        await app.save()
        app.submitted_data.permission_profile = permission_profile_model
        if app.approved_data is not None:
            app.approved_data.permission_profile = (
                await app.approved_data.permission_profile.fetch()
            )
        logger.info(app.approved_data)
        return schemas.AppReadWithAllData.model_validate(app.dict()).to_response()

    @staticmethod
    async def approve_app_background(
        app: models.App, frontend_file: AsyncIOMotorGridOut
    ) -> None:
        async with aiofiles.tempfile.TemporaryDirectory() as src_dir:
            frontend_file_path = pathlib.Path(src_dir) / frontend_file.filename
            frontend_src_path = pathlib.Path(settings.APP_STATIC_DIR) / app.name
            frontend_src_path_safe = ensure_safe_path(frontend_src_path)
            # TODO: this should not happen because we should have a check on app name
            if frontend_src_path_safe is None:
                logger.error("{} is invalid", frontend_src_path)
                return

            async with aiofiles.open(frontend_file_path, "wb") as file:
                data = await frontend_file.read()
                await file.write(data)

            def sync_func():
                frontend_src_path.parent.mkdir(parents=True, exist_ok=True)
                rmtree(str(frontend_src_path), ignore_errors=True)
                extract_archive(
                    str(frontend_file_path), outdir=str(frontend_src_path_safe)
                )
                logger.info(
                    "extract archive {} to {}",
                    frontend_file_path,
                    frontend_src_path_safe,
                )

            await run_in_threadpool(sync_func)

    @router.post(
        "/{app}/approve",
        description="Approve an app (site admin).",
        name="apps:approve",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.SITE))
        ],
    )
    async def approve_app(
        self,
        background_tasks: BackgroundTasks,
        app: models.App = Depends(get_path_app),
        db: AsyncDatabase = Depends(get_mongodb),
    ) -> schemas.StandardResponse[schemas.AppReadWithApprovedData]:
        if (
            app.submitted_data is None
            or app.submitted_data.backend is None
            or app.submitted_data.frontend is None
        ):
            raise BizError(ErrorCode.AppDataNotFoundError)
        submitted_permission_profile = (
            await app.submitted_data.permission_profile.fetch()
        )
        if app.approved_data is None:
            approved_permission_profile = models.PermissionProfile(
                read=submitted_permission_profile.read,
                write=submitted_permission_profile.write,
                arguments=submitted_permission_profile.arguments,
            )
            await approved_permission_profile.save()
            app.approved_data = models.AppData()
            app.approved_data.permission_profile = approved_permission_profile.to_ref()
        else:
            approved_permission_profile = (
                await app.approved_data.permission_profile.fetch()
            )
            approved_permission_profile.read = submitted_permission_profile.read
            approved_permission_profile.write = submitted_permission_profile.write
            approved_permission_profile.arguments = (
                submitted_permission_profile.arguments
            )
            await approved_permission_profile.save()

        app.approved_data.frontend = app.submitted_data.frontend
        app.approved_data.backend = app.submitted_data.backend
        app.approved_data.permission_model = app.submitted_data.permission_model
        app.approved = True
        await app.save()

        domains = (
            await models.DomainApp.find_many(
                models.DomainApp.app.id == app.id,
            )
            .aggregate(
                [
                    {"$group": {"_id": "$domain.$id"}},
                    {
                        "$lookup": {
                            "from": "domains",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "domains",
                        }
                    },
                    {"$replaceRoot": {"newRoot": {"$arrayElemAt": ["$domains", 0]}}},
                ],
                projection_model=models.Domain,
            )
            .to_list()
        )

        jobs = []
        for domain in domains:
            jobs.append(clear_cache(f"{domain.name}:authorized_entities:{app.name}"))
        await asyncio.gather(*jobs)

        frontend_file = await db.gridfs_bucket.open_download_stream(
            app.approved_data.frontend
        )
        background_tasks.add_task(self.approve_app_background, app, frontend_file)

        app.approved_data.permission_profile = approved_permission_profile
        return schemas.AppReadWithApprovedData.model_validate(app.dict()).to_response()

    @staticmethod
    async def build_app_background(
        app: models.App, backend_file: AsyncIOMotorGridOut
    ) -> schemas.AppBuild:
        async with aiofiles.tempfile.TemporaryDirectory() as src_dir:
            backend_file_path = pathlib.Path(src_dir) / backend_file.filename
            backend_src_path = pathlib.Path(src_dir) / "src"
            async with aiofiles.open(backend_file_path, "wb") as file:
                data = await backend_file.read()
                await file.write(data)

            def sync_func():
                extract_archive(str(backend_file_path), outdir=str(backend_src_path))
                logger.info(
                    "extract archive {} to {}", backend_file_path, backend_src_path
                )
                # image, output = register_app(app.name, "latest", str(backend_src_path))
                p = subprocess.run(
                    [
                        "docker",
                        "build",
                        "-t",
                        f"{app.name}:latest",
                        "--progress",
                        "plain",
                        ".",
                    ],
                    cwd=str(backend_src_path),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return schemas.AppBuild(
                    stdout=p.stdout,
                    stderr=p.stderr,
                    returncode=p.returncode,
                )

            return await run_in_threadpool(sync_func)

    @router.post(
        "/{app}/build",
        description="Build an app (site admin).",
        name="apps:build",
    )
    async def build_app(
        self,
        app: models.App = Depends(get_path_app),
        db: AsyncDatabase = Depends(get_mongodb),
    ) -> schemas.StandardResponse[schemas.AppBuild]:
        if app.approved_data is None or app.approved_data.backend is None:
            raise BizError(ErrorCode.AppBackendNotFoundError)
        backend_file = await db.gridfs_bucket.open_download_stream(
            app.approved_data.backend
        )
        # TODO: should we make it background?
        app_build = await self.build_app_background(app, backend_file)
        return schemas.AppBuild.model_validate(app_build.dict()).to_response()


@cbv(router)
class AppStatic:
    @router.get(
        "/{app}/static/{path:path}",
        description="Serve the frontend static files of the apps. "
        "We should move this part to an nginx container instead.",
        name="apps:static",
    )
    def get_static(
        self,
        # request: Request,
        app: str = Path(..., description="TODO"),
        path: str = Path(..., description="TODO"),
        # app_token: str = Cookie(None),
        # app_token_query: str = Query(None),
    ) -> FileResponse:
        # TODO: parse paths andread and return the right HTMLResponse
        # path_splits = [item for item in os.path.split(path) if item]
        # if not app_token and not app_token_query:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="An `app_token` should be given either in cookie or as a query parameter.",
        #     )
        # if app_token_query:
        #     app_token = app_token_query  # prioritize the token over cookies as it's more updated
        # payload = parse_jwt_token(app_token)
        # target_app = payload["app_id"]  # TODO: Change app_id to app_name later
        # if app_name != target_app:
        #     raise NotAuthorizedError(
        #         detail="The given app token is not for the target app"
        #     )
        # user = get_doc(User, user_id=payload["user_id"])
        # app = get_doc(StagedApp, name=app_name)
        # if app not in user.activated_apps:
        #     raise NotAuthorizedError(detail="The user have not installed the app")

        filepath = pathlib.Path(settings.APP_STATIC_DIR) / app / path
        filepath_safe = ensure_safe_path(filepath, must_exist=True)
        if filepath_safe is None or not filepath_safe.is_file():
            raise BizError(
                ErrorCode.AppStaticFileNotFoundError,
                error_message=str(pathlib.Path(app) / path),
            )
        # filepath = "static/" + app_name + "/" + path
        # if not os.path.exists(filepath):
        #     raise DoesNotExistError("File", filepath)
        resp = FileResponse(filepath)
        # TODO: Update app_token if it is about to expire.
        # resp.set_cookie(
        #     key="app_token", value=app_token, path="/brickapi/v1/apps/" + app_name
        # )
        # TODO: Find a way to get the path automatically
        return resp


EXCLUDED_HEADERS = [
    "content-encoding",
    "content-length",
    "transfer-encoding",
    "connection",
]


@cbv(router)
class AppApi:
    caddr_db: StrictRedis = Depends(get_app_management_redis_db)

    @router.api_route(
        "/{app}/api/{path:path}",
        methods=["GET", "POST", "DELETE", "PUT", "OPTIONS", "HEAD", "PATCH", "TRACE"],
        description="Call a backend api of an app.",
        name="apps:api",
    )
    async def app_api(
        self,
        request: Request,
        path: str = Path(description="Api endpoint in the app"),
        checker: Authorization = Depends(PermissionChecker()),
    ):
        if path.startswith("/"):
            path = path[1:]
        if checker.domain_user_app is None:
            raise BizError(ErrorCode.DomainUserAppNotFoundError)

        # TODO: cache cname or put in token
        cname = checker.domain_user_app.get_container_name()
        container_ip = get_container_ip(cname)

        if container_ip:
            container_url = (
                "http://" + container_ip + ":5000/"
            )  # TODO: Configure the port
        else:
            raise BizError(ErrorCode.AppContainerNotFoundError)

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
                content=request_data,
                follow_redirects=False,
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
