import itertools
from abc import ABC, abstractmethod
from typing import Any, List

from brick_server.playground import models, schemas


class SchedulingPolicyBase(ABC):
    def __init__(self, domain: models.Domain):
        self.domain = domain

    @abstractmethod
    async def blame(self, location: str, resource_type: str) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    async def find_victim(self, history: Any, notify_resource: schemas.NotifyResource):
        raise NotImplementedError()

    async def schedule(self, notify_resource: schemas.NotifyResource):
        entity_ids = await self.blame(
            notify_resource.location, notify_resource.resource_type
        )
        # get history with entity_ids (postgres)
        # SELECT entity_id, app, time FROM table WHERE entity_id IN (",".join(entity_ids));
        result = [[]]  # [(entity_id, [(app, time, ...)])]
        history = []
        for key, value in itertools.groupby(result, lambda x: x[0]):
            row = list(map(lambda x: x[1:], value))
            history.append((key, row))
        await self.find_victim(history, notify_resource)
