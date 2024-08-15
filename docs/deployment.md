# Deployment

## Clone the repository

SBOS is managed as a mono-repo. Clone the repository and work in the project directory.

```bash
git clone https://github.com/BrickSchema/playground
cd playground
```

## Configuration

Create a `.env` file in the project root directory. The file can be used to configure the playground server.
The detailed configurable items can be found [here](config/index.md).

```bash
touch .env
```

## Deploy the server

=== "Docker Compose (recommended)"

    In the playground directory, run

    ```bash
    docker-compose up --build -d # (1)!
    ```

    1.  make sure the context is correct if not using `docker-compose` but `docker build`
        and make sure the `docker-compose` version is at least `v2`

=== "Direct"

    (Not yet completed)

Then, open `http://localhost:9000/brickapi/v1/docs`. If the swagger API page is shown, congratulations!
Now you can move to the [next step](init.md) in initialize playground.
