from sbos.minimal.schemas.base import BaseModel

from sbos.playground.schemas.domain import DomainRead


class ResourceConstraintRead(BaseModel):
    entity_id: str
    value: float


class ResourceConstraintUpdate(BaseModel):
    entity_id: str
    value: float

class ResourceConstraintDelete(BaseModel):
    entity_id: str



class DomainResourceConstraintRead(ResourceConstraintRead):
    domain: DomainRead
