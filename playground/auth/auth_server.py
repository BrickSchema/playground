
from redis import StrictRedis
from starlette.responses import RedirectResponse
from pdb import set_trace as bp

from fastapi_utils.cbv import cbv
from fastapi import Depends, Header, HTTPException, Body, Query, Path
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import HTTPAuthorizationCredentials
from starlette.requests import Request

from brick_server.auth.auth_server import auth_router
from brick_server.auth.authorization import create_jwt_token
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.exceptions import DoesNotExistError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.models import get_doc

from ..app_management import app_management
from ..iptables_manager import iptables_manager
from ..dbs import get_app_management_redis_db
from ..services.models import app_name_desc
from ..models import App, User


@cbv(auth_router)
class LoginPerApp():
    redis_db: StrictRedis = Depends(get_app_management_redis_db)

    @auth_router.get('/app_login/{app_name}',
                    status_code=302,
                    description='TODO: Login point of a user for the app. This will redirect the user to Google login process. Once the login is done, the user will be redirected bck to `REDIRECT_URL + /<app_name>`.',
                    response_class=RedirectResponse,
                    tags=['Apps'],
                    )
    def app_login(self,
                  app_name: str = Path(..., description=app_name_desc),
                  token: HTTPAuthorizationCredentials = jwt_security_scheme,
                  ):
        # print("enter login per hosted app")
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, userid=jwt_payload['user_id'])
        app = get_doc(App, name=app_name)
        assert app in user.activated_apps # authorization

        app_token = create_jwt_token(app_name=app.name,
                                     user_id=user.userid,
                                     token_lifetime=app.token_lifetime,
                                     )
        redirect_url = app.callback_url + '?app_token=' + app_token.decode("utf-8")
        #container_name = app_management.spawn_app(app_name, user.userid.replace('@', 'at'))
        container_name = app_name + "-" + user.userid # TODO: this is for dev. use the above line.
        if container_name == '': #TODO: update the return value to None. or raise Execption
            print("app not found")
            raise DoesNotExistError(App, app_name)
        #TODO: Activate below.
        #iptables_manager.grant_host_access(app_management.get_container_id(container_name),
        #                                   redis_db.get(container_name), # TODO: make it injection.
        #                                   "tcp", # TODO: Make it configurable.
        #                                   "5001"
        #                                   )
        return RedirectResponse(redirect_url, status_code=302)
