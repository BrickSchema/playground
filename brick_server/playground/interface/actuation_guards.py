from abc import ABC, abstractmethod


class ActuationGuard(ABC):
    def __init__(self):
        self.priority = 0

    @abstractmethod
    def __call__(self, entity_id, value) -> bool:
        raise NotImplementedError()


class ActuationGuardIsOdd(ActuationGuard):
    def __init__(self):
        super().__init__()
        self.priority = 1

    def __call__(self, entity_id, value) -> bool:
        if not value.isdigit():
            raise ValueError()
        value = int(value)
        return value % 2 == 1


class ActuationGuardIsEven(ActuationGuard):
    def __init__(self):
        super().__init__()
        self.priority = 1

    def __call__(self, entity_id, value) -> bool:
        if not value.isdigit():
            raise ValueError()
        value = int(value)
        return value % 2 == 0


class ActuationGuardIsPrime(ActuationGuard):
    def __init__(self):
        super().__init__()
        self.priority = 2
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    def __call__(self, entity_id: str, value: str) -> bool:
        if not value.isdigit():
            raise ValueError()
        value = int(value)
        if value <= 0 or value > 50:
            raise ValueError()
        return value in self.primes


actuation_guards = {
    "is_odd": ActuationGuardIsOdd(),
    "is_even": ActuationGuardIsEven(),
    "is_prime": ActuationGuardIsPrime(),
}


def guard_actuation(guards, entity_id, value) -> bool:
    for guard_name in guards:
        if guard_name not in actuation_guards:
            # use next guard if not found
            continue
        try:
            return bool(actuation_guards[guard_name](entity_id, value))
        except Exception:
            # use next guard if the entity_id and value cannot be handled
            pass
    return False


# if __name__ == "__main__":
#     print(guard_actuation(1, 1))
#     print(guard_actuation(1, 2))
#     print(guard_actuation(1, 4))
#     print(guard_actuation(1, 51))
#     print(guard_actuation(1, 52))
