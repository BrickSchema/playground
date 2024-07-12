# Deployment

## Clone the repositories

First, we need to clone `sbos-minimal`, `sbos-playground`, `sbos-frontend`, and `genie-brickified` repos into a same directory.

```bash
mkdir brick
git clone https://github.com/BrickSchema/brick-example-server
git clone https://github.com/BrickSchema/playground
git clone
```

## Configuration

Create a `.env` file in the playground directory. The file can be used to configure the playground server.
The detailed configurable items can be found [here](config/index.md).

```bash
cd playground
touch .env

```

## Deploy the server

=== "Docker (recommended)"

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
