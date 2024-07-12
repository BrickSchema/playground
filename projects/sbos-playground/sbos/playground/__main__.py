import pathlib

import click
import uvicorn
from click_default_group import DefaultGroup
from loguru import logger

from sbos.playground.config.manager import settings


@click.group(cls=DefaultGroup, default="serve", default_if_no_args=True)
@click.help_option("--help", "-h")
def cli_group():
    pass


@click.command()
def serve() -> None:
    uvicorn.run(
        app="sbos.playground.app:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_WORKERS == 1 and settings.DEBUG,
        reload_dirs=[
            "../sbos-minimal/sbos/minimal",
            "sbos/playground",
        ],
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


@click.command()
def generate_docs():
    from sbos.minimal.config.settings import base as minimal_base
    from settings_doc.main import app
    from typer.testing import CliRunner

    from sbos.playground.config.settings import base as playground_base

    runner = CliRunner()
    docs_classes = [
        minimal_base.DatabaseMongoDBSettings,
        minimal_base.DatabaseRedisSettings,
        minimal_base.DatabaseTimescaleDBSettings,
        minimal_base.DatabaseGraphDBSettings,
        minimal_base.DatabaseInfluxDBSettings,
        minimal_base.AuthGeneralSettings,
        minimal_base.AuthCORSSettings,
        minimal_base.AuthGoogleOAuthSettings,
        minimal_base.BackendMinimalSettings,
        minimal_base.BackendBrickSettings,
        playground_base.BackendPlaygroundSettings,
    ]

    docs_generated_path = (
        pathlib.Path(__file__).parent.parent.parent.absolute() / "docs" / "generated"
    )
    docs_generated_path.mkdir(parents=True, exist_ok=True)

    for doc_class in docs_classes:
        class_path = f"{doc_class.__module__}.{doc_class.__qualname__}"
        output_path = docs_generated_path / f"{doc_class.__qualname__}.md"
        output_path.touch(exist_ok=True)

        logger.info("Generate docs for class {} in {}", class_path, output_path)
        result = runner.invoke(
            app,
            [
                "generate",
                "--class",
                class_path,
                "--output-format",
                "markdown",
                "--heading-offset",
                "2",
                "--update",
                str(output_path),
            ],
        )
        if result.exit_code != 0:
            logger.error("Failed! Error message: {}", result.stdout)


# @click.command()
# @click.option("--user-id", type=str, default="admin")
# @click.option("--app-name", type=str, default="")
# @click.option("--domain-name", type=str, default="")
# @click.option("--token-lifetime", type=int, default=0)
# @click.option("--create", is_flag=True)
# def generate_jwt(
#     user_id: str, app_name: str, domain_name: str, token_lifetime: int, create: bool
# ) -> None:
#     settings = config.init_settings(FastAPIConfig)
#     # print(settings)
#
#     from sbos.minimal.auth.authorization import create_user
#     from sbos.minimal.dbs import mongo_connection
#     from sbos.minimal.models import get_doc_or_none
#
#     from sbos.playground.auth.jwt import create_jwt_token
#     from sbos.playground.models import (
#         App,
#         Domain,
#         DomainUser,
#         DomainUserApp,
#         User,
#     )
#
#     _ = mongo_connection  # prevent import removed by pycln
#     if token_lifetime == 0:
#         token_lifetime = settings.jwt_expire_seconds
#
#     user = get_doc_or_none(User, user_id=user_id)
#     print(user)
#     domain = None
#     app = None
#     if user is None:
#         if create:
#             user = create_user(
#                 name=user_id, user_id=user_id, email=f"{user_id}@gmail.com"
#             )
#         else:
#             print("user not found")
#             exit(-1)
#     if domain_name:
#         domain = get_doc_or_none(Domain, name=domain_name)
#         if domain is None:
#             if create:
#                 domain = Domain(name=domain_name)
#                 domain.save()
#             else:
#                 print("domain not found")
#                 exit(-1)
#         domain_user = get_doc_or_none(DomainUser, domain=domain, user=user)
#         if domain_user is None:
#             if create:
#                 domain_user = DomainUser(domain=domain, user=user, is_admin=False)
#                 domain_user.save()
#             else:
#                 print("domain_user not found")
#                 exit(-1)
#
#         if app_name:
#             app = get_doc_or_none(App, name=app_name)
#             if app is None:
#                 if create:
#                     app = App(
#                         name=app_name,
#                         description="",
#                         approved=True,
#                         profile=None,
#                         permission_model="permission_model",
#                     )
#                     app.save()
#                 else:
#                     print("app not found")
#                     exit(-1)
#             domain_user_app = get_doc_or_none(
#                 DomainUserApp, domain=domain, user=user, app=app
#             )
#             if domain_user_app is None:
#                 if create:
#                     domain_user_app = DomainUserApp(domain=domain, user=user, app=app)
#                     domain_user_app.save()
#                 else:
#                     print("domain_user_app not found")
#                     exit(-1)
#
#     jwt = create_jwt_token(
#         domain=domain, user=user, app=app, token_lifetime=token_lifetime
#     )
#     print(jwt)


if __name__ == "__main__":
    cli_group.add_command(serve)
    cli_group.add_command(generate_docs)
    # cli_group.add_command(generate_jwt)
    cli_group()
