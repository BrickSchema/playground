import arrow
from brick_server.minimal.auth.authorization import (
    authenticated,
    jwt_security_scheme,
    parse_jwt_token,
)
from brick_server.minimal.exceptions import AlreadyExistsError, DoesNotExistError
from brick_server.minimal.models import get_doc
from brick_server.minimal.schemas import IsSuccess
from fastapi import Body, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger
from rdflib import URIRef

from brick_server.playground import models, schemas
from brick_server.playground.app_management.app_management import (
    spawn_app,
    stop_container,
)
from brick_server.playground.auth.authorization import (
    get_domain_app,
    get_domain_user_app,
    get_user_from_jwt,
)
from brick_server.playground.services.models import (
    ActivatedApps,
    UserRelationshipsRequest,
    UserResponse,
)

user_router = InferringRouter()


@cbv(user_router)
class UserRelationResource:
    @user_router.post(
        "/relationship",
        description="Update a user's relationship",
        response_model=IsSuccess,
        tags=["Users"],
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
        tags=["Users"],
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
            activated_apps=[app.name for app in user.activated_apps],
            registration_time=arrow.get(user.registration_time).datetime,
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

    @user_router.get(
        "/domains/{domain}/apps/{app}",
        status_code=200,
        description="Install an app for the user.",
        tags=["Users"],
    )
    def get_app(
        self,
        domain_user_app: models.DomainUserApp = Depends(get_domain_user_app),
    ):
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
        domain_user_app_start: schemas.DomainUserAppStart = Body(),
    ):
        if domain_user_app.running:
            raise AlreadyExistsError("app", domain_user_app.app.name)
        container_name = spawn_app(
            domain_user_app.app.name, domain_user_app.user.user_id.replace("@", "at")
        )
        logger.info(container_name)
        domain_user_app.running = True
        # TODO: examine the arguments
        domain_user_app.arguments = domain_user_app_start.arguments
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
        if not domain_user_app.running:
            raise DoesNotExistError("app", domain_user_app.app.name)
        container_name = (
            domain_user_app.app.name
            + "-"
            + domain_user_app.user.user_id.replace("@", "at")
        )
        try:
            stop_container(container_name)
        except Exception as e:
            logger.exception(e)
            # raise e
        domain_user_app.running = False
        domain_user_app.save()
        return schemas.DomainUserApp.from_orm(domain_user_app)
