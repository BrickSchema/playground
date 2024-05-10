from enum import Enum
from typing import TYPE_CHECKING, Union

from brick_server.minimal.utilities.exceptions import ErrorCode as MinimalErrorCode


def extend_enum(inherited_enum):
    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper


@extend_enum(MinimalErrorCode)
class ErrorCode(str, Enum):
    # App Errors
    AppNotFoundError = "AppNotFoundError"
    AppNotApprovedError = "AppNotApprovedError"
    AppAlreadyExistsError = "AppAlreadyExistsError"
    AppDataNotFoundError = "AppDataNotFoundError"
    AppStaticFileNotFoundError = "AppStaticFileNotFoundError"
    AppContainerNotFoundError = "AppContainerNotFoundError"

    # Domain Errors
    DomainAppNotFoundError = "DomainAppNotFoundError"
    DomainAppAlreadyExistsError = "DomainAppAlreadyExistsError"
    DomainUserNotFoundError = "DomainUserNotFoundError"
    DomainUserAlreadyExistsError = "DomainUserAlreadyExistsError"
    DomainUserAppNotFoundError = "DomainUserAppNotFoundError"
    DomainUserAppAlreadyExistsError = "DomainUserAppAlreadyExistsError"
    PermissionProfileNotFoundError = "PermissionProfileNotFoundError"
    PermissionProfileAlreadyExistsError = "PermissionProfileAlreadyExistsError"
    ResourceConstraintNotFoundError = "ResourceConstraintNotFoundError"
    DomainPreActuationPolicyNotFoundError = "DomainPreActuationPolicyNotFoundError"
    DomainPreActuationPolicyAlreadyExistsError = (
        "DomainPreActuationPolicyAlreadyExistsError"
    )


if TYPE_CHECKING:
    ErrorCode = Union[ErrorCode, MinimalErrorCode]
