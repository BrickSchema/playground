from sbos.minimal.interfaces.cache import use_cache
from sbos.minimal.interfaces.graphdb import graphdb

from sbos.playground.interfaces.actuation_guard.base import ActuationGuard


class ActuationGuardRangeChecker(ActuationGuard):
    def __init__(self):
        super().__init__()
        self.priority = 1

    async def __call__(self, entity_id, value) -> bool:
        query = """
SELECT * WHERE {{
    <{entity_id}> <http://www.ontotext.com/owlim/entity#id> ?id
}} ORDER BY ?id
        """.format(
            entity_id=entity_id
        )
        cache_key = f"Center_Hall:range_checker:{entity_id}"

        async def fallback_func():
            return await graphdb.query("Center_Hall", query)

        res = await use_cache(cache_key, fallback_func)
        return True
