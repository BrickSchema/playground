# Deployment

## Clone the repository

SBOS is managed as a mono-repo. Clone the repository and work in the project directory.

```bash
git clone https://github.com/BrickSchema/playground
cd projects/sbos-playground
```

## Configuration

Playground can be configured with various options. 
Please follow this [guide](config/index.md) to configure it.


## Deploy the server

=== "Docker Compose (recommended)"

    In the playground directory (`projects/sbos-playground`), run

    ```bash
    docker-compose up --build -d # (1)!
    ```

    1.  make sure the context is correct if not using `docker-compose` but `docker build`
        and make sure the `docker-compose` version is at least `v2`

    In development mode, run
    
    ```bash
    docker compose -f docker-compose.yml -f docker-compose-dev.yml up -d --build
    ```

=== "Direct"
    
    (Not yet completed)
    
    The project is managed by `poetry` and `poe`.
    
    ```bash
    poetry install
    poe 
    ```

Then, open <http://localhost:9000/brickapi/v1/docs>. If the swagger API page is shown, congratulations!
Now you can move to the [next step](init.md) in initialize playground.
