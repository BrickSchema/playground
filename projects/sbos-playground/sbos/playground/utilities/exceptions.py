from enum import Enum
from typing import TYPE_CHECKING, Union

from sbos.minimal.utilities.exceptions import (
    BizError as MinimalBizError,
    ErrorCode as MinimalErrorCode,
    ErrorShowType,
)


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


class BizError(MinimalBizError):
    def __init__(
        self,
        error_code: ErrorCode,
        error_message: str = "",
        show_type: ErrorShowType = ErrorShowType.ErrorMessage,
    ):
        super().__init__(error_code, error_message, show_type)


# replace the definition of error in minimal for correct documentation in openapi.json
import sbos.minimal.utilities.exceptions

sbos.minimal.utilities.exceptions.BizError = BizError
sbos.minimal.utilities.exceptions.ErrorCode = ErrorCode


if TYPE_CHECKING:
    ErrorCode = Union[ErrorCode, MinimalErrorCode]
