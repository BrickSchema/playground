from brick_server.minimal.exceptions import AlreadyExistsError, DoesNotExistError
from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from brick_server.playground import models
from brick_server.playground.auth.authorization import get_app, get_domain

domain_router = InferringRouter(tags=["Domains"])


@cbv(domain_router)
class DomainAppRoute:
    @domain_router.post("/{domain}/apps/{app}")
    async def add_app(
        self,
        domain: models.Domain = Depends(get_domain),
        app: models.App = Depends(get_app),
    ):
        if not app.approved:
            raise DoesNotExistError("app", app.name)
        domain_app = models.DomainApp(
            domain=domain,
            app=app,
        )
        try:
            domain_app.save()
        except Exception:
            # TODO: catch the precise already exist exception
            raise AlreadyExistsError("app", app.name)
