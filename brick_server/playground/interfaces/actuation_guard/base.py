from abc import ABC, abstractmethod


class ActuationGuard(ABC):
    def __init__(self):
        self.priority = 0

    @abstractmethod
    def __call__(self, entity_id, value) -> bool:
        raise NotImplementedError()
