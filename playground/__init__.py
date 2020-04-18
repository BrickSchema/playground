from brick_server import app as brick_server_app
from brick_server.dependencies  import update_dependency_supplier


from .auth.authorization import evaluate_app_user
from .services.apps import app_router
from .services.market_apps import marketapp_router
from .services.users import user_router as user_app_router

update_dependency_supplier('auth_logic', evaluate_app_user)

app = brick_server_app

app.include_router(app_router, prefix='/brickapi/v1/apps')
app.include_router(marketapp_router, prefix='/brickapi/v1/market_apps')
app.include_router(user_app_router, prefix='/brickapi/v1/user_apps')
