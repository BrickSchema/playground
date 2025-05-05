from typing import List

from fastapi import Body, Depends, Query, Request
from fastapi_restful.cbv import cbv
from loguru import logger
from sbos.minimal.securities.checker import PermissionChecker
from sbos.minimal.services.user import router

from sbos.playground import models, schemas
from sbos.playground.interfaces.app_management import (
    get_container,
    rm_container,
    spawn_app,
    start_container,
    stop_container,
)
from sbos.playground.schemas import DockerStatus, PermissionScope, PermissionType
from sbos.playground.securities.auth import (
    Authorization,
    create_jwt_token,
    get_domain_app,
    get_domain_user,
    get_token_user,
)
from sbos.playground.utilities.dependencies import (
    get_domain_user_profiles,
    get_path_app,
    get_path_domain,
)
from sbos.playground.utilities.exceptions import BizError, ErrorCode


@router.post(
    "/init_superuser",
    description="Set the current user as superuser. "
    "Can only be called when there is no superuser in the site.",
    name="users:init_superuser",
)
async def init_superuser(
    user: models.User = Depends(get_token_user),
) -> schemas.StandardResponse[schemas.UserRead]:
    superuser = await models.User.find_one(models.User.is_superuser == True)
    if superuser is None:
        user.is_superuser = True
        await user.save()
    return schemas.UserRead.model_validate(user.dict()).to_response()


@cbv(router)
class UserResource:

    @router.get(
        "/domains/{domain}/permissions",
        description="Get all authorized permissions of the token in domain.",
        name="users:list_domain_permissions",
    )
    async def list_domain_user_permissions(
        self,
        request: Request,
        domain: models.Domain = Depends(get_path_domain),
        checker: Authorization = Depends(
            PermissionChecker(permission_scope=PermissionScope.ENTITY)
        ),
        types: List[str] = Query(None),
    ) -> schemas.StandardResponse[schemas.AuthorizedEntities]:
        import time

        start = time.time()

        is_admin = await checker.check_admin_domain()
        # if not is_admin:
        read, read_prefixes = await checker.get_all_authorized_entities(
            PermissionType.READ
        )
        write, write_prefixes = await checker.get_all_authorized_entities(
            PermissionType.WRITE
        )
        # write = set()
        if types:
            prefixes = read_prefixes
            prefixes.update(write_prefixes)
            filtered = await checker.filter_entities_by_types(
                read.union(write), types, prefixes
            )
            read = checker.intersect_types_dict(read, filtered)
            write = checker.intersect_types_dict(write, filtered)
        else:
            read = {"": list(read)}
            write = {"": list(write)}
        # else:
        #     read = []
        #     write = []
        # timer: _TimingStats = getattr(request.state, TIMER_ATTRIBUTE)
        # timer.take_split()
        return schemas.AuthorizedEntities(
            read=read,
            write=write,
            is_admin=is_admin,
            response_time=1000 * (time.time() - start),
        ).to_response()

    @router.get(
        "/domains/{domain}/profiles",
        dependencies=[
            Depends(PermissionChecker(permission_scope=schemas.PermissionScope.USER))
        ],
        name="users:list_domain_user_profiles",
    )
    async def list_domain_user_profiles(
        self,
        domain_user_profiles: list[models.PermissionProfile] = Depends(
            get_domain_user_profiles
        ),
    ) -> schemas.StandardListResponse[schemas.DomainUserProfileRead]:
        return schemas.StandardListResponse(
            [
                schemas.DomainUserProfileRead.model_validate(profile.dict())
                for profile in domain_user_profiles
            ]
        )


@cbv(router)
class UserListApps:
    domain: models.Domain = Depends(get_path_domain)
    user: models.User = Depends(get_token_user)
    domain_user: models.DomainUser = Depends(get_domain_user)

    @router.get(
        "/domains/{domain}/apps",
        description="View apps that user activated in a domain.",
        name="users:list_apps",
    )
    async def list_apps(
        self,
    ) -> schemas.StandardListResponse[schemas.DomainUserAppRead]:
        domain_user_apps = await models.DomainUserApp.find_many(
            models.DomainUserApp.domain.id == self.domain.id,
            models.DomainUserApp.user.id == self.user.id,
            fetch_links=True,
            nesting_depth=1,
        ).to_list()
        return schemas.StandardListResponse(
            [
                schemas.DomainUserAppRead.model_validate(domain_user_app.dict())
                for domain_user_app in domain_user_apps
            ]
        )

    # @router.delete(
    #     "/apps",
    #     status_code=200,
    #     description="Deactivate all the apps for this user (for development)",
    #     response_model=IsSuccess,
    # )
    # def deactivate_all_apps(
    #     self,
    #     token: HTTPAuthorizationCredentials = jwt_security_scheme,
    # ):
    #     jwt_payload = parse_jwt_token(token.credentials)
    #     user = get_doc(models.User, user_id=jwt_payload["user_id"])
    #     user.activated_apps = []
    #     user.save()
    #
    #     return IsSuccess()


@cbv(router)
class UserApps:
    domain: models.Domain = Depends(get_path_domain)
    user: models.User = Depends(get_token_user)
    app: models.App = Depends(get_path_app)
    # domain_user: models.DomainUser = Depends(get_domain_user)
    # domain_app: models.DomainUser = Depends(get_domain_app)
    checker: PermissionChecker = Depends(
        PermissionChecker(permission_scope=schemas.PermissionScope.USER)
    )

    async def get_domain_user_app(self) -> models.DomainUserApp:
        domain_user_app = await models.DomainUserApp.find_one(
            models.DomainUserApp.domain.id == self.domain.id,
            models.DomainUserApp.user.id == self.user.id,
            models.DomainUserApp.app.id == self.app.id,
            fetch_links=True,
            nesting_depth=1,
        )
        if domain_user_app is None:
            raise BizError(ErrorCode.DomainUserAppNotFoundError)
        return domain_user_app

    def get_response(
        self, domain_user_app: models.DomainUserApp
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app.domain = self.domain
        domain_user_app.user = self.user
        domain_user_app.app = self.app
        return schemas.DomainUserAppRead.model_validate(
            domain_user_app.dict()
        ).to_response()

    @router.post(
        "/domains/{domain}/apps/{app}",
        description="Get an app for the user.",
        name="users:install_app",
    )
    async def install_app(
        self,
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user = await get_domain_user(self.domain, self.user)
        if domain_user is None:
            raise BizError(ErrorCode.DomainUserNotFoundError)
        domain_app = await get_domain_app(self.domain, self.app)
        if domain_app is None:
            raise BizError(ErrorCode.DomainAppNotFoundError)

        domain_user_app = models.DomainUserApp(
            domain=self.domain,
            user=self.user,
            app=self.app,
            status="",
        )
        try:
            await domain_user_app.save()
        except Exception:
            # TODO: catch the precise already exist exception
            raise BizError(ErrorCode.DomainUserAppAlreadyExistsError)

        return self.get_response(domain_user_app)

    @staticmethod
    async def _operate_container(
        domain_user_app: models.DomainUserApp, operation: str, start: bool = True
    ) -> bool:
        container_name = domain_user_app.get_container_name()
        container = get_container(container_name)
        try:
            if operation == "create" or operation == "start":
                await domain_user_app.fetch_all_links()
                token = await create_jwt_token(
                    domain=domain_user_app.domain,
                    user=domain_user_app.user,
                    app=domain_user_app.app,
                    domain_user_app=domain_user_app,
                )
                logger.info("app token: {}", token)
                domain_user_app.token = token
            if container is None:
                if operation == "create" or operation == "start":
                    container = spawn_app(
                        domain_user_app.app.name,
                        container_name,
                        start=start,
                        token=domain_user_app.token,
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

        logger.info("{} container: {}", operation, container)

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

    @router.get(
        "/domains/{domain}/apps/{app}",
        description="Get an app for the user.",
        name="users:get_app",
    )
    async def get_app(
        self,
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app = await self.get_domain_user_app()
        if await self._operate_container(domain_user_app, "get"):
            await domain_user_app.save()
        return self.get_response(domain_user_app)

    @router.patch(
        "/domains/{domain}/apps/{app}",
        description="Set the arguments of an app for the user.",
        name="users:set_app_arguments",
    )
    async def set_app_arguments(
        self,
        domain_user_app_init: schemas.DomainUserAppArguments = Body(),
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        logger.info(domain_user_app_init.arguments)
        domain_user_app = await self.get_domain_user_app()
        domain_user_app.arguments = domain_user_app_init.arguments
        await domain_user_app.save()
        return self.get_response(domain_user_app)

    @router.delete(
        "/domains/{domain}/apps/{app}",
        description="Uninstall an app for the user.",
        name="users:uninstall_app",
    )
    async def uninstall_app(self) -> schemas.StandardResponse[schemas.Empty]:
        domain_user_app = await self.get_domain_user_app()
        await self._operate_container(domain_user_app, "remove")
        await domain_user_app.delete()
        return schemas.StandardResponse()

    @router.post(
        "/domains/{domain}/apps/{app}/create",
        description="Create the container of an app for the user.",
        name="users:create_app_container",
    )
    async def create_app_container(
        self,
        # domain_user_app_create: schemas.DomainUserAppCreate = Body(),
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app = await self.get_domain_user_app()
        # if domain_user_app.status == DockerStatus.RUNNING:
        #     raise AlreadyExistsError("app", domain_user_app.app.name)
        await self._operate_container(domain_user_app, "create")
        # TODO: examine the arguments
        # domain_user_app.arguments = domain_user_app_create.arguments
        await domain_user_app.save()
        return self.get_response(domain_user_app)

    @router.post(
        "/domains/{domain}/apps/{app}/start",
        description="Start the container of an app for the user.",
        name="users:start_app_container",
    )
    async def start_app_container(
        self,
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app = await self.get_domain_user_app()
        if await self._operate_container(domain_user_app, "start"):
            await domain_user_app.save()
        return self.get_response(domain_user_app)

    @router.post(
        "/domains/{domain}/apps/{app}/stop",
        description="Stop the container of an app for the user.",
        name="users:stop_app_container",
    )
    async def stop_app_container(
        self,
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app = await self.get_domain_user_app()
        if await self._operate_container(domain_user_app, "stop"):
            await domain_user_app.save()
        return self.get_response(domain_user_app)

    @router.post(
        "/domains/{domain}/apps/{app}/remove",
        description="Remove the container of an app for the user.",
        name="users:remove_app_container",
    )
    async def remove_app_container(
        self,
    ) -> schemas.StandardResponse[schemas.DomainUserAppRead]:
        domain_user_app = await self.get_domain_user_app()
        if await self._operate_container(domain_user_app, "remove"):
            await domain_user_app.save()
        return self.get_response(domain_user_app)
