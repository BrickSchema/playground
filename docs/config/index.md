# Configuration

## Setup

### Env File

Usually a `.env` file is created in the directory **`projects/sbos-playground`**. 
The file can be used to configure the playground server.

!!! warning

    Make sure you place the `.env` file in the correct directory.


!!! example

    If the default server port should be changed from `9000` to `10000`, 
    the following line can be added in the `.env` file:
    
    ```dotenv title=".env"
    SERVER_PORT=10000
    ```

### Environment Variables

Alternatively, environment variables can also be used, and its priority is higher.

!!! example

    ```bash
    export SERVER_PORT=10000
    ```

### Other

Configuration can also be setup in other places.

For detailed environment variables precedence rules, check the section [Environment Variables Precedence](#environment-variables-precedence).


## Configuration List

!!! note

    If docker-compose is used to deploy the service, and the configuration entry is not listed in the compose file,
    the entry should be added to the "environment" section manually.


There are three types of configurations:

+ [Database](db.md): Database connection 
+ [Authorization](auth.md): JWT, CORS, OAuth2
+ [Backend](backend.md): Server host, port, url, and etc.

## Environment Variables Precedence

=== "Docker Compose (recommended)"

    > The order of precedence (highest to lowest) is as follows:
    >
    > 1. Set using docker compose run -e in the CLI.
    > 2. Set with either the environment or env_file attribute but with the value interpolated from your shell or an environment file. (either your default .env file, or with the --env-file argument in the CLI).
    > 3. Set using just the environment attribute in the Compose file.
    > 4. Use of the env_file attribute in the Compose file.
    > 5. Set in a container image in the ENV directive. Having any ARG or ENV setting in a Dockerfile evaluates only if there is no Docker Compose entry for environment, env_file or run --env.
    > 
    > Source: <https://docs.docker.com/compose/environment-variables/envvars-precedence>{target="_blank"}

=== "Direct"

    > Even when using a dotenv file, pydantic will still read environment variables as well as the dotenv file, environment variables will always take priority over values loaded from a dotenv file.
    >
    > Source: <https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support>{target="_blank"}

    

