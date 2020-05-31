
from redis import StrictRedis
from starlette.responses import RedirectResponse
from pdb import set_trace as bp

from fastapi_utils.cbv import cbv
from fastapi import Depends, Header, HTTPException, Body, Query, Path
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import HTMLResponse, Response
from starlette.requests import Request

from brick_server.auth.auth_server import auth_router
from brick_server.auth.authorization import create_jwt_token
from brick_server.auth.authorization import auth_scheme, parse_jwt_token, authorized, authorized_arg, R, O
from brick_server.exceptions import DoesNotExistError, AlreadyExistsError
from brick_server.services.models import jwt_security_scheme, IsSuccess
from brick_server.models import get_doc

from ..app_management import app_management
from ..iptables_manager import iptables_manager
from ..dbs import get_app_management_redis_db
from ..services.models import app_name_desc
from ..models import StagedApp, User
from .models import AppLoginResponse


@cbv(auth_router)
class LoginPerApp():
    caddr_db: StrictRedis = Depends(get_app_management_redis_db)

    @auth_router.get('/app_login/{app_name}',
                    status_code=200,
                    description='TODO: Login point of a user for the app. This will redirect the user to Google login process. Once the login is done, the user will be redirected bck to `REDIRECT_URL + /<app_name>`.',
                    #response_model=AppLoginResponse,
                    tags=['Apps'],
                    )
    def app_login(self,
                  app_name: str = Path(..., description=app_name_desc),
                  token: HTTPAuthorizationCredentials = jwt_security_scheme,
                  external: bool = False,
                  ):
        jwt_payload = parse_jwt_token(token.credentials)
        user = get_doc(User, user_id=jwt_payload['user_id'])
        app = get_doc(StagedApp, name=app_name)
        assert app in user.activated_apps # authorization

        app_token = create_jwt_token(app_name=app.name,
                                     user_id=user.user_id,
                                     token_lifetime=app.token_lifetime,
                                     )
        try:
            container_name = app_management.spawn_app(app_name, user.user_id.replace('@', 'at'))
        except Exception as e:
            container_name = '{app_name}-{user_id}'.format(app_name=app_name, user_id=user.user_id.replace('@', 'at'))
            if f'Conflict. The container name "/{container_name}"' in str(e):
                print(e)
                pass
            else:
                raise e

        iptables_manager.grant_host_access(app_management.get_container_id(container_name),
                                           self.caddr_db.get(container_name),
                                           "tcp", # TODO: Make it configurable.
                                           "5001"
                                           )

        if not external:
            redirect_url = f'/brickapi/v1/apps/{app_name}/static/index.html?app_token_query=' + app_token.decode('utf-8')
            resp = Response(content=redirect_url)
            return resp
        else:
            resp = RedirectResponse(app.callback_url)
            resp.set_cookie(key='app_token', value=app_token.decode('utf-8'))
            return resp
        #return AppLoginResponse(redirect_url=app.callback_url,
        #                        app_token=app_token.decode('utf-8'),
        #                        )
