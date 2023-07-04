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
        reload=settings.debug,
        log_level="debug",
        reload_dirs=[
            "../brick-server-minimal/brick_server/minimal",
            "brick_server/playground",
        ],
    )


@cli.command()
@click.option("--user-id", type=str, default="admin")
@click.option("--app-name", type=str, default="brickapp")
@click.option("--domain", type=str, default="bldg")
@click.option("--token-lifetime", type=int, default=0)
@click.option("--create-user", is_flag=True)
def generate_jwt(
    user_id: str, app_name: str, domain: str, token_lifetime: int, create_user: bool
) -> None:
    settings = config.init_settings(FastAPIConfig)
    print(settings)

    from brick_server.minimal.auth.authorization import create_user
    from brick_server.minimal.dbs import mongo_connection
    from brick_server.minimal.models import get_doc_or_none

    from brick_server.playground.auth.jwt import create_jwt_token
    from brick_server.playground.models import App, Domain, User

    _ = mongo_connection  # prevent import removed by pycln
    if token_lifetime == 0:
        token_lifetime = settings.jwt_expire_seconds

    user = get_doc_or_none(User, user_id=user_id)
    domain = get_doc_or_none(Domain, name=domain)
    app = get_doc_or_none(App, name=app_name)
    if create_user and user is None:
        user = create_user(name=user_id, user_id=user_id, email=f"{user_id}@gmail.com")
    if domain is None or app is None:
        click.echo("error: domain or app not found!")
        return

    jwt = create_jwt_token(
        domain=domain, user=user, app=app, token_lifetime=token_lifetime
    )
    print(jwt)


if __name__ == "__main__":
    cli_group.add_command(serve)
    cli_group.add_command(generate_jwt)
    cli_group()
