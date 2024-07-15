from typing import Optional

from beanie import PydanticObjectId

from sbos.minimal.schemas.base import BaseModel


class DomainRead(BaseModel):
    id: PydanticObjectId
    name: str
    initialized: bool


class DomainCreate(BaseModel):
    name: str


class DomainUpdate(BaseModel):
    name: Optional[str] = None
