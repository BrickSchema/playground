import itertools
from typing import Any, List

from brick_server.playground import schemas
from brick_server.playground.scheduling_policy.base import SchedulingPolicyBase


class SchedulingPolicyNaive(SchedulingPolicyBase):
    async def blame(self, location: str, resource_type: str) -> List[str]:
        return ["additionalProp1", "additionalProp3"]

    async def find_victim(
        self, history: List[Any], notify_resource: schemas.NotifyResource
    ):
        result = sorted(history, key=lambda x: ((x[1], x[2]), x[3]))
        app_latest_use_time = []
        for key, value in itertools.groupby(result, key=lambda x: (x[1], x[2])):
            app_latest_use_time.append((list(value))[-1])
        app_latest_use_time.sort(key=lambda x: x[-1])
        victim_app = app_latest_use_time[-1][1:3]
        victim_entity = app_latest_use_time[-1][0]
        return [victim_app], [victim_entity]
