from typing import List

import arrow
from brick_server.minimal.auth.authorization import (
    authenticated,
    jwt_security_scheme,
    parse_jwt_token,
)
from brick_server.minimal.auth.checker import PermissionChecker
from brick_server.minimal.exceptions import AlreadyExistsError
from brick_server.minimal.models import get_doc
from brick_server.minimal.schemas import IsSuccess, PermissionScope, PermissionType
from fastapi import Body, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger
from rdflib import URIRef

from brick_server.playground import models, schemas
from brick_server.playground.app_management.app_management import (
    get_container,
    rm_container,
    spawn_app,
    start_container,
    stop_container,
)
from brick_server.playground.auth.authorization import (
    Authorization,
    get_domain_app,
    get_domain_user_app,
    get_user_from_jwt,
)
from brick_server.playground.schemas import DockerStatus
from brick_server.playground.services.models import (
    ActivatedApps,
    UserRelationshipsRequest,
    UserResponse,
)

user_router = InferringRouter(tags=["Users"])


@cbv(user_router)
class UserRelationResource:
    @user_router.post(
        "/relationship",
        description="Update a user's relationship",
        response_model=IsSuccess,
    )
    @authenticated
    async def add_user_relation(
        self,
        relation_req: UserRelationshipsRequest = Body(..., description="TODO"),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(models.User, user_id=jwt_payload["user_id"])
        # TODO: Interpret the graph
        for p, o in relation_req.relationships:
            # TODO: Verify p and o are valid
            await self.brick_db.add_triple(URIRef(user.user_id), p, o)
        return IsSuccess()


@cbv(user_router)
class UserResource:
    @user_router.get(
        "/",
        status_code=200,
        description="Get User info",
        response_model=UserResponse,
    )
    def get_user_info(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(models.User, user_id=jwt_payload["user_id"])
        return UserResponse(
            name=user.name,
            user_id=user.user_id,
            email=user.email,
            is_admin=user.is_admin,
            is_approved=user.is_approved,
            # activated_apps=[app.name for app in user.activated_apps],
            registration_time=arrow.get(user.registration_time).datetime,
        )

    @user_router.get(
        "/domains/{domain}/permissions",
        status_code=200,
        description="Get token permissions in domain",
    )
    async def get_permission(
        self,
        checker: Authorization = Depends(
            PermissionChecker(permission_scope=PermissionScope.ENTITY)
        ),
        types: List[str] = Query([]),
    ) -> schemas.AuthorizedEntities:
        is_admin = checker.check_admin_domain()
        if not is_admin:
            read = await checker.get_all_authorized_entities(PermissionType.READ)
            write = await checker.get_all_authorized_entities(PermissionType.WRITE)
            # write = set()
            if types:
                filtered = await checker.filter_entities_by_types(
                    read.union(write), types
                )
                read.intersection_update(filtered)
                write.intersection_update(filtered)
        else:
            read = []
            write = []
        return schemas.AuthorizedEntities(
            read=list(read), write=list(write), is_admin=is_admin
        )


@cbv(user_router)
class UserApps:
    @user_router.get(
        "/apps",
        status_code=200,
        description="View apps that user activated.",
        response_model=ActivatedApps,
        tags=["Users"],
    )
    def get_activated_apps(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(models.User, user_id=jwt_payload["user_id"])
        resp = ActivatedApps(activated_apps=[app.name for app in user.activated_apps])

        return resp

    @user_router.delete(
        "/apps",
        status_code=200,
        description="Deactivate all the apps for this user (for development)",
        response_model=IsSuccess,
        tags=["Users"],
    )
    def deactivate_all_apps(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(models.User, user_id=jwt_payload["user_id"])
        user.activated_apps = []
        user.save()

        return IsSuccess()

    @user_router.post(
        "/domains/{domain}/apps/{app}",
        status_code=200,
        description="Get an app for the user.",
        tags=["Users"],
    )
    def install_app(
        self,
        # activation_req: ActivationRequest = Body(...),
        user: models.User = Depends(get_user_from_jwt),
        domain_app: models.DomainApp = Depends(get_domain_app),
        # token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ) -> IsSuccess:
        domain_user_app = models.DomainUserApp(
            domain=domain_app.domain,
            user=user,
            app=domain_app.app,
            running=False,
        )
        try:
            domain_user_app.save()
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("app", "name")

        # jwt_payload = parse_jwt_token(token.credentials)
        # user = get_doc(User, user_id=jwt_payload["user_id"])
        # app_name = activation_req.app_name
        # app = get_doc(models.DomainApp, domain=, name=app_name)
        # if app in user.activated_apps:
        #     raise AlreadyExistsError(StagedApp, app_name)
        # app_id = app.app_id
        # user.activated_apps.append(app)
        # user.save()
        # return IsSuccess(reason="Already activated")

    @staticmethod
    def _operate_container(
        domain_user_app: models.DomainUserApp, operation: str, start: bool = True
    ) -> bool:
        container_name = domain_user_app.get_container_name()
        container = get_container(container_name)
        try:
            if container is None:
                if operation == "create" or operation == "start":
                    container = spawn_app(
                        domain_user_app.app.name, container_name, start=start
                    )
            else:
                if operation == "start" and container.status != DockerStatus.RUNNING:
                    start_container(container_name)
                elif (
                    operation == "create"
                    and start
                    and container.status != DockerStatus.RUNNING
                ):
                    start_container(container_name)
                elif operation == "stop":
                    stop_container(container_name)
                elif operation == "remove":
                    rm_container(container_name)
        except Exception as e:
            logger.exception(e)

        if container is None:
            status = DockerStatus.EXITED
            container_id = ""
        else:
            status = container.status
            container_id = container.id

        if (
            domain_user_app.status != status
            or domain_user_app.container_id != container_id
        ):
            domain_user_app.status = status
            domain_user_app.container_id = container_id
            return True
        return False

    @user_router.get(
        "/domains/{domain}/apps/{app}",
        status_code=200,
        description="Get an app for the user.",
        tags=["Users"],
    )
    def get_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
    ):
        if self._operate_container(domain_user_app, "get"):
            domain_user_app.save()
        return schemas.DomainUserApp.from_orm(domain_user_app)

    @user_router.post(
        "/domains/{domain}/apps/{app}/create",
        status_code=200,
        description="Create an app for the user.",
        # response_model=AppResponse,
        tags=["Users"],
    )
    def create_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
        domain_user_app_create: schemas.DomainUserAppCreate = Body(),
    ):
        # if domain_user_app.status == DockerStatus.RUNNING:
        #     raise AlreadyExistsError("app", domain_user_app.app.name)

        self._operate_container(domain_user_app, "create")
        # TODO: examine the arguments
        domain_user_app.arguments = domain_user_app_create.arguments
        domain_user_app.save()

        return schemas.DomainUserApp.from_orm(domain_user_app)

    @user_router.post(
        "/domains/{domain}/apps/{app}/start",
        status_code=200,
        description="Start an app for the user.",
        # response_model=AppResponse,
        tags=["Users"],
    )
    def start_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
    ):
        if self._operate_container(domain_user_app, "start"):
            domain_user_app.save()
        return schemas.DomainUserApp.from_orm(domain_user_app)

    @user_router.post(
        "/domains/{domain}/apps/{app}/stop",
        status_code=200,
        description="Stop an app for the user.",
        # response_model=AppResponse,
        tags=["Users"],
    )
    def stop_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
    ):
        if self._operate_container(domain_user_app, "stop"):
            domain_user_app.save()
        return schemas.DomainUserApp.from_orm(domain_user_app)

    @user_router.post(
        "/domains/{domain}/apps/{app}/remove",
        status_code=200,
        description="Remove an app for the user.",
        # response_model=AppResponse,
        tags=["Users"],
    )
    def remove_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
    ):
        if self._operate_container(domain_user_app, "remove"):
            domain_user_app.save()
        return schemas.DomainUserApp.from_orm(domain_user_app)
