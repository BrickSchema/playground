from brick_server.playground.interface.actuation_guard_naive import (
    ActuationGuardIsEven,
    ActuationGuardIsOdd,
    ActuationGuardIsPrime,
)

# from loguru import logger

actuation_guards = {
    "is_odd": ActuationGuardIsOdd(),
    "is_even": ActuationGuardIsEven(),
    "is_prime": ActuationGuardIsPrime(),
}


# def guard_actuation(guards, entity_id, value) -> bool:
#     for guard_name in guards:
#         if guard_name not in actuation_guards:
#             # use next guard if not found
#             logger.warning("{} not found in actuation guards", guard_name)
#             continue
#         try:
#             result = bool(actuation_guards[guard_name](entity_id, value))
#             if not result:
#                 return False
#         except Exception:
#             # use next guard if the entity_id and value cannot be handled
#             pass
#     return True


# if __name__ == "__main__":
#     print(guard_actuation(1, 1))
#     print(guard_actuation(1, 2))
#     print(guard_actuation(1, 4))
#     print(guard_actuation(1, 51))
#     print(guard_actuation(1, 52))
