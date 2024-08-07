import itertools
from typing import Any, List

from sbos.playground import schemas
from sbos.playground.interfaces.scheduling_policy.base import SchedulingPolicyBase


class SchedulingPolicyNaive(SchedulingPolicyBase):
    async def blame(self, entity_id: str) -> List[str]:
        return ["additionalProp1", "additionalProp3"]

    async def find_victim(
        self, history: List[Any], notify_resource: schemas.ResourceConstraintRead
    ):
        result = sorted(history, key=lambda x: ((x[1], x[2]), x[4]))
        app_latest_use_time = []
        for key, value in itertools.groupby(result, key=lambda x: (x[1], x[2])):
            app_latest_use_time.append((list(value))[-1])
        app_latest_use_time.sort(key=lambda x: x[4])
        victim_app = app_latest_use_time[-1][3]
        victim_entity = app_latest_use_time[-1][0]
        return [victim_app], [victim_entity]
