import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.timing import add_timing_middleware
from loguru import logger
from sbos.minimal.utilities.logging import init_logging, intercept_all_loggers

from sbos.playground.config.errors import register_error_handlers
from sbos.playground.config.events import (
    execute_backend_server_event_handler,
    terminate_backend_server_event_handler,
)
from sbos.playground.config.manager import settings
from sbos.playground.securities.auth import auth_logic
from sbos.playground.utilities.dependencies import update_dependency_supplier

update_dependency_supplier(auth_logic)


def initialize_backend_application() -> fastapi.FastAPI:
    init_logging()
    intercept_all_loggers()
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    add_timing_middleware(app, record=logger.info)
    app.logger = logger

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    register_error_handlers(app)

    from sbos.playground.services import router as api_endpoint_router, redirect_docs

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)
    app.get("/", include_in_schema=False)(redirect_docs)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()


# app.mount("/brickapi/v1/appstatic", StaticFiles(directory="static"), name="static")
