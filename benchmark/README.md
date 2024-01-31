# Brick Server Playground Microbenchmark

## Setup

### With cache

```bash
CACHE=true docker compose -p brick-server-playground up -d
```

### Without cache

```bash
CACHE=false docker compose -p brick-server-playground up -d
```

## Run

### Init database

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py init
```

### Capability Derivation

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test capability
```
