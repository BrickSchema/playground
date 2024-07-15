from sbos.minimal.schemas.base import BaseModel


class ActuationResult(BaseModel):
    success: bool
    detail: str = ""


class ActuationResults(BaseModel):
    results: list[ActuationResult] = []
    response_time: dict = {}
