from fastapi import APIRouter
from sbos.minimal.config.manager import settings
from sbos.minimal.services.auth import router as auth_router
from sbos.minimal.services.data import router as data_router
from sbos.minimal.services.query import router as query_router
from starlette.responses import RedirectResponse

from sbos.playground.services.actuation import router as actuation_router
from sbos.playground.services.app import router as app_router
from sbos.playground.services.domain import router as domain_router
from sbos.playground.services.profile import router as profile_router
from sbos.playground.services.user import router as user_router

router = APIRouter()


@router.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse(url=settings.DOCS_URL)


router.include_router(router=auth_router)
router.include_router(router=query_router)
router.include_router(router=user_router)
router.include_router(router=domain_router)
router.include_router(router=actuation_router)
router.include_router(router=data_router)
router.include_router(router=app_router)
router.include_router(router=profile_router)
