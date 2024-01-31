import click
import uvicorn
from click_default_group import DefaultGroup
from fastapi_rest_framework import cli, config

from brick_server.playground.config import FastAPIConfig


@click.group(cls=DefaultGroup, default="serve", default_if_no_args=True)
@click.help_option("--help", "-h")
def cli_group():
    pass


@cli.command()
def serve() -> None:
    settings = config.init_settings(FastAPIConfig)
    uvicorn.run(
        "brick_server.playground.app:app",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
        reload=settings.workers == 1 and settings.debug,
        workers=settings.workers,
        log_level="debug",
        reload_dirs=[
            "../brick-server-minimal/brick_server/minimal",
            "brick_server/playground",
        ],
    )


@cli.command()
@click.option("--user-id", type=str, default="admin")
@click.option("--app-name", type=str, default="")
@click.option("--domain-name", type=str, default="")
@click.option("--token-lifetime", type=int, default=0)
@click.option("--create", is_flag=True)
def generate_jwt(
    user_id: str, app_name: str, domain_name: str, token_lifetime: int, create: bool
) -> None:
    settings = config.init_settings(FastAPIConfig)
    # print(settings)

    from brick_server.minimal.auth.authorization import create_user
    from brick_server.minimal.dbs import mongo_connection
    from brick_server.minimal.models import get_doc_or_none

    from brick_server.playground.auth.jwt import create_jwt_token
    from brick_server.playground.models import (
        App,
        Domain,
        DomainUser,
        DomainUserApp,
        User,
    )

    _ = mongo_connection  # prevent import removed by pycln
    if token_lifetime == 0:
        token_lifetime = settings.jwt_expire_seconds

    user = get_doc_or_none(User, user_id=user_id)
    print(user)
    domain = None
    app = None
    if user is None:
        if create:
            user = create_user(
                name=user_id, user_id=user_id, email=f"{user_id}@gmail.com"
            )
        else:
            print("user not found")
            exit(-1)
    if domain_name:
        domain = get_doc_or_none(Domain, name=domain_name)
        if domain is None:
            if create:
                domain = Domain(name=domain_name)
                domain.save()
            else:
                print("domain not found")
                exit(-1)
        domain_user = get_doc_or_none(DomainUser, domain=domain, user=user)
        if domain_user is None:
            if create:
                domain_user = DomainUser(domain=domain, user=user, is_admin=False)
                domain_user.save()
            else:
                print("domain_user not found")
                exit(-1)

        if app_name:
            app = get_doc_or_none(App, name=app_name)
            if app is None:
                if create:
                    app = App(
                        name=app_name,
                        description="",
                        approved=True,
                        profile=None,
                        permission_model="permission_model",
                    )
                    app.save()
                else:
                    print("app not found")
                    exit(-1)
            domain_user_app = get_doc_or_none(
                DomainUserApp, domain=domain, user=user, app=app
            )
            if domain_user_app is None:
                if create:
                    domain_user_app = DomainUserApp(domain=domain, user=user, app=app)
                    domain_user_app.save()
                else:
                    print("domain_user_app not found")
                    exit(-1)

    jwt = create_jwt_token(
        domain=domain, user=user, app=app, token_lifetime=token_lifetime
    )
    print(jwt)


if __name__ == "__main__":
    cli_group.add_command(serve)
    cli_group.add_command(generate_jwt)
    cli_group()
