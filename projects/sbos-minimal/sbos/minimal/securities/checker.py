import abc
import asyncio
from typing import Callable, Dict, Set, Tuple, Union

from fastapi import Body, Depends, Query

from sbos.minimal.schemas import PermissionScope, PermissionType, TimeseriesData
from sbos.minimal.utilities.dependencies import dependency_supplier
from sbos.minimal.utilities.descriptions import Descriptions
from sbos.minimal.utilities.exceptions import BizError, ErrorCode


class PermissionCheckerBase(abc.ABC):
    def __init__(
        self,
        permission_type: PermissionType = PermissionType.NA,
        permission_scope: PermissionScope = PermissionScope.ENTITY,
    ):
        self.permission_type = permission_type
        self.permission_scope = permission_scope

    @staticmethod
    async def call_auth_logic(
        auth_logic,
        entity_ids: Set[str],
        permission_type: PermissionType,
        permission_scope: PermissionScope,
    ):
        if hasattr(auth_logic, "__call__"):
            auth_logic_func = auth_logic.__call__
        else:
            auth_logic_func = auth_logic
        if asyncio.iscoroutinefunction(auth_logic_func):
            result = await auth_logic_func(
                entity_ids, permission_type, permission_scope
            )
        else:
            result = auth_logic_func(entity_ids, permission_type, permission_scope)
        if not result:
            raise BizError(ErrorCode.UnauthorizedError)
        return auth_logic


class PermissionChecker(PermissionCheckerBase):
    async def __call__(
        self,
        # token: HTTPAuthorizationCredentials = jwt_security_scheme,
        auth_logic: Callable[
            [Set[str], PermissionType, PermissionScope], bool
        ] = Depends(dependency_supplier.auth_logic),
    ):
        return await self.call_auth_logic(
            auth_logic, set(), self.permission_type, self.permission_scope
        )


class PermissionCheckerWithEntityId(PermissionCheckerBase):
    async def __call__(
        self,
        # token: HTTPAuthorizationCredentials = jwt_security_scheme,
        auth_logic: Callable[
            [Set[str], PermissionType, PermissionScope], bool
        ] = Depends(dependency_supplier.auth_logic),
        entity_id: str = Query(..., description=""),
    ):
        return await self.call_auth_logic(
            auth_logic, {entity_id}, self.permission_type, self.permission_scope
        )


class PermissionCheckerWithData(PermissionCheckerBase):
    @staticmethod
    def get_entity_ids(data: TimeseriesData) -> Set[str]:
        rows = data.data
        columns = data.columns
        uuid_idx = columns.index("uuid")
        uuids = {row[uuid_idx] for row in rows}
        return uuids

    async def __call__(
        self,
        # token: HTTPAuthorizationCredentials = jwt_security_scheme,
        auth_logic: Callable[
            [Set[str], PermissionType, PermissionScope], bool
        ] = Depends(dependency_supplier.auth_logic),
        data: TimeseriesData = Body(..., description=Descriptions.timeseries_data),
    ):
        entity_ids = self.get_entity_ids(data)
        return await self.call_auth_logic(
            auth_logic, entity_ids, self.permission_type, self.permission_scope
        )


class PermissionCheckerActuation(PermissionCheckerBase):
    async def __call__(
        self,
        # token: HTTPAuthorizationCredentials = jwt_security_scheme,
        auth_logic: Callable[
            [Set[str], PermissionType, PermissionScope], bool
        ] = Depends(dependency_supplier.auth_logic),
        actuation_request: Dict[str, Union[Tuple[str], Tuple[str, str]]] = Body(...),
    ):
        entity_ids = set(actuation_request.keys())
        return await self.call_auth_logic(
            auth_logic, entity_ids, self.permission_type, self.permission_scope
        )
