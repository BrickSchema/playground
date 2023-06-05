import uvicorn
from fastapi_rest_framework import cli, config

from brick_server.playground.config import FastAPIConfig


@cli.command()
def main() -> None:
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



if __name__ == "__main__":
    main()
