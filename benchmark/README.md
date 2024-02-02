# Brick Server Playground Artifact

This artifact is for ICCPS'24 reproducibility evaluations on our paper titled "Playground: A Safe Building Operating System". The focus of this paper is the presentation of a novel building operating system design abstraction. Therefore quantitative reproducibility applies solely to the microbenchmarks (Sec V.D) in this paper --- the script provided below will reproduce the experiment and results presented there. Since our microbenchmark majorly focus on the time consumption of a few critical system operations with and without caching and is highly dependendant on the hardware of the underlying platform, it is expectable that the time measurements will not be exactly the same as in the paper --- instead, the relative pattern with and without caching will be preserved and should be the main observation.

## Setup

*Our system has been tested on various distros of Linux. We anticipate it would work with Windows but not guaranteed.*

Prepare your platform with [Docker](https://docs.docker.com/engine/install/) and [Docker-compose](https://docs.docker.com/compose/install/). Get your working directory as where you place all provided files.

Caching is an option set at the system booting phase. To start playground with cache:

```bash
CACHE=true docker compose -p brick-server-playground up -d
```

or without cache

```bash
CACHE=false docker compose -p brick-server-playground up -d
```

*You may execute the commands above directly to switch to the other option without turning down the entire docker compose.*

Depending on your platform, this step may take up to a few minutes in the background.

## Run Microbenchmarks

### Init

Before running microbenchmarks, we must initialize the system first. Make sure the system has fully start up before executing the below command, otherwise you may see errors and the process will be aborted automatically. Upon errors, try to execute this command again after a while e.g. 30s. The execution of the initialization may take up to ten minutes depending on your platform. (A thousand users need to be intialized in the capabability derivation microbenchmark.). Please do not terminate it unless it is aborted itself. Don't worry --- there is a progress bar!

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py init
```

Below are commands for each microbenmark respectively. We have progress bar during execution set up for each of them as well to help you understand the progress since the total runtime could be up to several minutes for each of them depending on your platform.

### Capability Derivation

Reproduce the microbenchmark on capability derivation (Fig 7 left, Sec V.D second paragraph and appendix E).

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test capability
```

### Validator mapping
Reproduce the microbenchmark on validator mapping (Fig 7 right, Sec V.D second paragraph and appendix E).

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test validator
```

### Resource Spec Retrieval
Reproduce tThe microbenchmark on Resource Spec Retrieval (Sec V.D third paragraph and appendix E).

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test resource
```

### Range Checker Validator
Reproduce the microbenchmark on Range Checker Validator (Sec V.D third paragraph and appendix E).

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test range
```

### Power Predictor Validator
Reproduce the microbenchmark on Power Predictor Validator (Sec V.D third paragraph and appendix E).

```bash
docker exec -it brick-server-playground-core-1 python benchmark/benchmark.py test predictor
```

## Note

The last measurement described in the last paragraph of Sec V.D would require actual deployment of our system on real buildings and is not presentable here. 

Readers with interest/knowledge in Brick ontology could edit the relevant queries for validator mappings and permission profiles in `benchmark.py` (check inline code comments) to extend the existing microbenmarks. The Brick representation of the building that we are working with (`center_hall.ttl`) is also provided as a reference.
