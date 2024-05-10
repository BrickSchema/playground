# import subprocess
from shlex import split
from typing import Optional, TextIO, Tuple

import redis
from docker.models.containers import Container
from docker.models.images import Image

import docker
from brick_server.playground.config.manager import settings
from brick_server.playground.schemas import DockerStatus

docker_client = docker.from_env()


app_management_redis_db = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DATABASE,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)

caddr_db = app_management_redis_db
# TODO: Think about how to use injection model
# TODO: Think about how to use asyncio. (aioredis)


def get_cname(app_name, user_id):
    return app_name + "-" + user_id.replace("@", "at")


def register_app(
    app_name: str,
    ver: str,
    src_dir: str,
    # start_cmd: str,
    # build_env: str,
    # port: int or None = None,
    # build_cmd: str = "",
) -> Tuple[Image, TextIO]:
    """
    Register an new app or update an existing app as runnable docker images.

    Parameters
    ----------
    app_name
        desired name of the application
    ver
        version number, could be a regular version number string or 'latest'
    src_dir
        source code directory location
    start_cmd
        starting command as the entry point for the docker
    build_env
        desired building environment i.e. parent docker image)
    port: optional
        port number to be exposed
    build_cmd: optional
        the command used prebuilding to setup the env

    Returns
    -------


    Examples
    --------
    >>> register_app("webapp", "latest", "hello_world_web","python index.py", "python:3", 5000)

    """
    # type check
    if not isinstance(app_name, str):
        raise TypeError("app name is expected to be str")
    elif app_name == "":
        raise ValueError("app_name is expected to be a none empty string")
    if not isinstance(ver, str):
        raise TypeError("version number is expected to be str")
    if not isinstance(src_dir, str):
        raise TypeError("source directory is expected to be str")
    # if not isinstance(build_cmd, str):
    #     raise TypeError("building command is expected to be str")
    # if not isinstance(start_cmd, str):
    #     raise TypeError("starting command is expected to be str")
    # if not isinstance(build_env, str):
    #     raise TypeError("building environment is expected to be str")
    # if not isinstance(port, int):
    #     raise TypeError("port is expected to be int")

    # generate corresponding Dockerfile in the root directory of the source code
    # with open(src_dir + "/Dockerfile", "w") as f:
    #     contents = [
    #         "FROM " + build_env + "\n",
    #         "COPY . /" + app_name + "\n",
    #         "WORKDIR /" + app_name + "\n",
    #     ]
    #     if build_cmd != "":
    #         contents += ["RUN " + build_cmd + "\n"]
    #     if port is not None:
    #         contents += ["EXPOSE " + str(port) + "\n"]
    #     contents += [parse_start_cmd(start_cmd)]
    #     f.writelines(contents)

    # build the docker image
    # subprocess.run(["docker", "build", src_dir, "-t", app_name+":"+ver])
    return docker_client.images.build(path=src_dir, tag=app_name + ":" + ver, rm=True)


def parse_start_cmd(start_cmd: str) -> str:
    """a helper function to parse a str command into ENTRYPOINT[List[str]] format"""
    l = split(start_cmd)
    return "ENTRYPOINT [" + ", ".join('"' + x + '"' for x in l) + "]"


def spawn_app(
    app_name: str,
    container_name: str,
    token: str,
    arguments: str = "",
    start: bool = True,
) -> Container:
    """
    Run the target application docker image under specific user with given arguments for that application

    Parameters
    ----------
    app_name
        the application name, same as the one used to register
    container_name
        the name of the continer with format {app_name}-{user_id}-{objectid}
    token
        the api token used by the container
    arguments: List[str], optional
        additional arguments for the application
    start: bool, optional
        whether to start the app after creation

    Returns
    -------
    Container
        the container object which accommodates the spawned app

    Examples
    --------
    >>> print(spawn_app("toy_web", "3", "--port 5555"))
    toy_web3

    """
    # return run_container(app_name, app_name + "-" + user_id, app_name, ["-it", "-m", "64MB", "--network", "isolated_nw", "--rm"], arguments)

    # type check
    if not isinstance(app_name, str):
        raise TypeError("app name is expected to be str")
    elif app_name == "":
        raise ValueError("app_name is expected to be a none empty string")
    if not isinstance(container_name, str):
        raise TypeError("container name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be a none empty string")
    if not isinstance(arguments, str):
        raise TypeError("arguments is expected to be str")

    # default parameter, could be modified to kwargs in the future for more flexible settings
    # parameters = ["-d", "-m", "64MB", "--network", "isolated_nw", "--rm"]
    # container naming is subject to changes
    # container_name = app_name + "-" + user_id
    # parse the arguments to List(str)
    arguments = split(arguments)
    # run the docker image in container
    # subprocess.run(["docker", "run"]+parameters+["--name", container_id, app_name]+arguments)
    container = get_container(container_name)
    if container is None:
        container = docker_client.containers.create(
            image=app_name,
            command=arguments,
            detach=True,
            mem_limit="64m",
            network=settings.ISOLATED_NETWORK_NAME,
            name=container_name,
            environment={"BRICK_SERVER_API_TOKEN": token},
            # auto_remove=True,
        )
    if start and container.status != DockerStatus.RUNNING:
        container.start()
    # docker_client.containers.run(image=app_name, command=arguments, stdin_open=True, mem_limit='64m', network='isolated_nw', remove=True, name=container_id)
    # create corresponding iptables chain based on container iid
    # iptables_manager.create_chain(get_container_id(container_name))

    # create entry in database
    caddr_db.set(container_name, get_container_ip(container_name))
    return container


# def run_container(container_id:str, image_name:str, parameters:List[str]=None, arguments:List[str]=None) -> str:
#   """helper function for spawn_app"""
# subprocess.run(["docker", "ps"])
# docker run -p 9999:9999 -it --rm --name client_remote client_to_remote python ./client.py 172.17.0.1 2222


def stop_container(container_name: str) -> Container:
    """
    stop the container with the name
    Note when --rm is included in parameters for run by default, this container will be removed after it's stopped.

    Parameters
    ----------
    container_name
        name of the container, returned by spawn_app

    Returns
    -------
    Container

    """
    if not isinstance(container_name, str):
        raise TypeError("container name is expected to be str")
    container = docker_client.containers.get(container_name)
    container.stop()
    # iptables_manager.delete_chain(get_container_id(container_name))
    caddr_db.delete(container_name)
    return container


def start_container(container_name: str) -> Container:
    """
    start the container with the name

    Parameters
    ----------
    container_name
        name of the container, returned by spawn_app

    Returns
    -------
    Container

    """
    if not isinstance(container_name, str):
        raise TypeError("container name is expected to be str")
    # subprocess.run(["docker", "start", container_id])
    container = docker_client.containers.get(container_name)
    container.start()
    return container


def rm_container(container_name: str) -> Container:
    """force remove the container with the name"""
    if not isinstance(container_name, str):
        print("Container Name is Expected to be Str")
        return
    # subprocess.run(["docker", "rm", "--force", container_id])
    container = docker_client.containers.get(container_name)
    container.remove(force=True)
    # iptables_manager.delete_chain(get_container_id(container_name))
    return container


def get_container_ip(container_name: str) -> str:
    """
    Get container ip address based on its name

    Parameters
    ----------
    container_name
        name of the container, returned by spawn_app

    Returns
    -------
    str
        the ip address in str

    """
    # rt = subprocess.run(split("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "+
    #                         container_id),stdout=subprocess.PIPE)
    # return rt.stdout.decode("UTF-8")[:-1]
    return docker_client.containers.get(container_name).attrs["NetworkSettings"][
        "Networks"
    ][settings.ISOLATED_NETWORK_NAME]["IPAddress"]


def get_container(container_name: str) -> Optional[Container]:
    try:
        return docker_client.containers.get(container_name)
    except Exception:
        return None


def get_container_id(container_name: str) -> str:
    """
    Get container id (truncated) based on its name

    Parameters
    ----------
    container_name
        name of the container, returned by spawn_app

    Returns
    -------
    str
        the id in str

    """
    c = docker_client.containers.get(container_name)
    return c.id[:12]  # truncated id
