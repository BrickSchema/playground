import time

from brick_server.minimal.auth.jwt import sign_jwt_token
from brick_server.minimal.models import get_doc_or_none
from fastapi_rest_framework.config import settings

from brick_server.playground import models


def create_jwt_token(
    domain: models.Domain,
    user: models.User,
    app: models.App,
    token_lifetime: int = settings.jwt_expire_seconds,
):
    domain_user_app = get_doc_or_none(
        models.DomainUserApp, domain=domain.id, user=user.id, app=app.id
    )
    payload = {
        "user_id": user.user_id,
        "exp": time.time() + token_lifetime,
        "app_name": app.name,
        "domain": domain.name,
        "domain_user_app": str(domain_user_app.id) if domain_user_app else None,
    }
    return sign_jwt_token(payload, token_lifetime)