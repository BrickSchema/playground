from uuid import uuid4


def gen_uuid():
    return str(uuid4())


from fastapi import HTTPException, Path
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from brick_server.minimal.auth.authorization import (
    authorized_admin,
    jwt_security_scheme,
    parse_jwt_token,
)
from brick_server.minimal.exceptions import NotAuthorizedError

# from brick_server.configs import configs
from brick_server.minimal.models import get_doc, get_docs
from brick_server.minimal.schemas import IsSuccess

from ..models import (  # TODO: Change naming conventino for mongodb models
    StagedApp,
    User,
)
from .models import (
    AppApprovalRequest,
    AppNames,
    PendingApprovalsResponse,
    app_name_desc,
)

# from ..dependencies import get_brick_db, dependency_supplier


admin_router = InferringRouter(prefix="/admins")


@cbv(admin_router)
class AppApproval:
    @admin_router.post(
        "/app_approval",
        status_code=200,
        description="Approve an app's access pattern",
        response_model=IsSuccess,
        tags=["Admin"],
    )
    @authorized_admin
    async def approve_app(
        self,
        approval_request: AppApprovalRequest,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ) -> IsSuccess:
        parsed = parse_jwt_token(token.credentials)
        user_id = parsed["user_id"]
        app = get_doc(StagedApp, app_id=approval_request.app_name)
        if user_id not in app.pending_approvals:
            raise HTTPException(
                status_code=400,
                detail='The user "{user_id}" either is not the right person to approve this app or already approaved it.',
            )
        app.pending_approvals = [
            admin for admin in app.pending_approvals if admin != user_id
        ]
        app.save()
        return IsSuccess()

    @admin_router.get(
        "/app_approval/{app_name}",
        status_code=200,
        description="Get a list of admins that have not approved the app yet",
        response_model=PendingApprovalsResponse,
        tags=["Admin"],
    )
    async def check_app_approval(
        self,
        app_name: str = Path(..., description=app_name_desc),
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ):
        # TODO: Implement Logic
        return PendingApprovalsResponse(admins=["TODO:AN_ADMIN_NAME"])

    @admin_router.get(
        "/app_approval",
        status_code=200,
        description="List the names of apps pending approval on the current admin",
        response_model=AppNames,
        tags=["Admin"],
    )
    async def list_pending_apps(
        self,
        token: HTTPAuthorizationCredentials = jwt_security_scheme,
    ) -> AppNames:
        # TODO: Implement Logic
        parsed = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=parsed["user_id"])
        if not user.is_admin:
            raise NotAuthorizedError(detail="The user is not an admin")
        app_names = [
            app.name
            for app in get_docs(StagedApp, pending_approvals__contains=user.user_id)
        ]
        return app_names
