from brick_server.playground.interface.actuation_guard_base import ActuationGuard


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
