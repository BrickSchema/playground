from sbos.minimal.schemas.base import BaseModel


class ActuationResult(BaseModel):
    entity_id: str
    success: bool
    detail: str = ""


class ActuationResults(BaseModel):
    results: list[ActuationResult] = []
    response_time: dict = {}
