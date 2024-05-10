from brick_server.minimal.schemas.base import BaseModel

from brick_server.playground.schemas.domain import DomainRead


class ResourceConstraintRead(BaseModel):
    entity_id: str
    value: float


class ResourceConstraintUpdate(BaseModel):
    value: float


class DomainResourceConstraintRead(ResourceConstraintRead):
    domain: DomainRead
