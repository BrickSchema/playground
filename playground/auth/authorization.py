from typing import Dict, Any, Optional, Type, TypeVar, List
from bson import ObjectId
from mongoengine import Document

from brick_server.auth.authorization import parse_jwt_token
from brick_server.models import get_doc, get_docs
from brick_server.services.models import jwt_security_scheme
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials

from ..models import StagedApp, User, Domain, DomainUser, DomainOccupancy, DomainRole

SEP = "^#$%"


def make_permission_key(user_id, app_name, entity_id):
    return user_id + SEP + app_name + SEP + entity_id


def check_permissions(entity_ids, user, app, permission_required):
    for entity_id in entity_ids:
        perm_key = make_permission_key(user.user_id, app.name, entity_id)
        perm = r.get(perm_key)
        if perm is None:
            raise exceptions.Unauthorized(
                "The token does not have any permission over {0}".format(entity_id)
            )
        perm = perm.decode("utf-8")
        perm_type, perm_start_time, perm_end_time = decode_permission_val(perm)
        if permission_required not in perm_type:
            raise exceptions.Unauthorized(
                "The token does not have `{0}` permission for {1}".format(
                    permission_required, entity_id
                )
            )
        curr_time = time.time()
        if curr_time < perm_start_time or curr_time > perm_end_time:
            raise exceptions.Unauthorized("The token is not valid at the current time.")
    return True


def evaluate_app_user(action_type, target_ids, *args, **kwargs):
    jwt_payload = parse_jwt_token(kwargs["token"].credentials)
    app = get_doc(StagedApp, name=jwt_payload["app_id"])
    user = get_doc(User, user_id=jwt_payload["user_id"])
    check_permissions(target_ids, user, app, action_type)


def get_doc_or_none(doc_type: Any, **query):
    try:
        return get_doc(doc_type, **query)
    except doc_type.DoesNotExist:
        return None


def get_jwt_payload(
    token: HTTPAuthorizationCredentials = jwt_security_scheme,
) -> Dict[str, Any]:
    return parse_jwt_token(token.credentials)


def get_current_user(jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)) -> User:
    return get_doc(User, user_id=jwt_payload["user_id"])


def get_staged_app(jwt_payload: Dict[str, Any] = Depends(get_jwt_payload)) -> StagedApp:
    return get_doc(StagedApp, name=jwt_payload["app_id"])


def get_domain_id(
    domain: str = Path(..., description="ObjectId of the domain")
) -> ObjectId:
    return ObjectId(domain)
    # return get_doc(Domain, _id=domain)


def get_domain_user(
    user: User = Depends(get_current_user), domain_id: ObjectId = Depends(get_domain_id)
) -> Optional[DomainUser]:
    return get_doc_or_none(DomainUser, user=user.id, domain=domain_id)


def get_domain_role(
    domain_id: ObjectId = Depends(get_domain_id),
    role_name: str = "basic",
) -> Optional[DomainRole]:
    return get_doc_or_none(DomainRole, domain=domain_id, role_name=role_name)


def get_domain_occupancies(
    user: User = Depends(get_current_user), domain_id: ObjectId = Depends(get_domain_id)
) -> List[DomainOccupancy]:
    return get_docs(DomainOccupancy, user=user.id, domain=domain_id)


class Authorization:
    def __init__(
        self,
        user: User = Depends(get_current_user),
        domain_id: Optional[ObjectId] = None,
    ) -> None:
        self.user = user
        self.domain_id = domain_id
        self.domain_occupancies = ...
        self.domain_user = ...
        self.domain_roles = {}

    def check_entity_by_location(
        self,
        location: str,
        entity: str,
        permission: str,
        domain_role: DomainRole,
    ):
        # return entity in basic permission of location
        return True

    def is_entity_in_location(self, location: str, entity: str):
        # query graph
        return True

    def check_in_locations_by_role_names(self, zipped, entity: str, permission: str):
        for location, role_name in zipped:
            if self.is_entity_in_location(location, entity):
                if (self.domain_id, role_name) not in self.domain_roles:
                    self.domain_roles[(self.domain_id, role_name)] = get_domain_role(
                        self.domain_id, role_name
                    )
                domain_role = self.domain_roles[(self.domain_id, role_name)]
                if domain_role is None:
                    continue
                if self.check_entity_by_location(
                    location=self.domain_occupancies.location,
                    entity=entity,
                    permission=permission,
                    domain_role=domain_role,
                ):
                    return True

    def check(self, entity: str, permission: str) -> bool:
        # if the user is site admin, grant all permissions
        if self.user.is_admin:
            return True

        # check permission in domain occupancy list
        if self.domain_occupancies is ...:
            self.domain_occupancies = get_domain_occupancies(self.user, self.domain_id)

        locations = [
            domain_occupancy.location for domain_occupancy in self.domain_occupancies
        ]
        role_names = ["basic"] * len(locations)
        if self.check_in_locations_by_role_names(
            zip(locations, role_names), entity, permission
        ):
            return True

        # get domain user info
        if self.domain_user is ...:
            self.domain_user = get_domain_user(self.user, self.domain_id)
        if self.domain_user is None:
            return False
        if self.domain_user.is_superuser:
            return True

        # check permission by domain user roles
        if self.check_in_locations_by_role_names(
            self.domain_user.roles.items(), entity, permission
        ):
            return True

        return False
