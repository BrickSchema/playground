from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi_users import exceptions as fastapi_users_exceptions
from pydantic import ValidationError
from sbos.minimal.config.errors import (
    business_error_handler,
    catch_exceptions_middleware,
    fastapi_users_error_handler,
    http_error_handler,
    validation_error_handler,
)

from sbos.playground.utilities.exceptions import BizError


def register_error_handlers(backend_app: FastAPI) -> None:
    backend_app.add_exception_handler(
        fastapi_users_exceptions.FastAPIUsersException, fastapi_users_error_handler
    )
    backend_app.add_exception_handler(BizError, business_error_handler)
    backend_app.add_exception_handler(ValidationError, validation_error_handler)
    backend_app.add_exception_handler(HTTPException, http_error_handler)
    backend_app.middleware("http")(catch_exceptions_middleware)
