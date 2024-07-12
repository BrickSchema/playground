import subprocess
from shlex import split


def create_chain(container_name: str):
    """
    Create iptables chains with the same name as the container name into DOCKER-USER chain and INPUT chain

    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    Returns
    -------
    None

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    cmd = "sudo iptables -N " + container_name + "-extn"
    subprocess.run(split(cmd))
    cmd = "iptables -I DOCKER-USER -j " + container_name + "-extn"
    subprocess.run(split(cmd))
    cmd = "sudo iptables -N " + container_name + "-host"
    subprocess.run(split(cmd))
    cmd = "iptables -I INPUT -j " + container_name + "-host"
    subprocess.run(split(cmd))


def delete_chain(container_name: str):
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")

    revoke_all_access(container_name)

    cmd = "iptables -D DOCKER-USER -j " + container_name + "-extn"
    subprocess.run(split(cmd))
    cmd = "sudo iptables -X " + container_name + "-extn"
    subprocess.run(split(cmd))

    cmd = "iptables -D INPUT -j " + container_name + "-host"
    subprocess.run(split(cmd))
    cmd = "sudo iptables -X " + container_name + "-host"
    subprocess.run(split(cmd))


def grant_external_access(
    container_name: str,
    container_ip: str,
    protocol: str = "",
    dst_ip: str = "",
    dst_port: str = "",
) -> None:
    """
    Grant the target container access to external host

    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    container_ip
        ip addr of the container i.e. returned by app_management.get_container_ip
    protocol: optional
        access protocol, could be either tcp or udp
    dst_ip: optional
        destination ip address, use '' if don't want to specify
    dst_port: optional
        destination port, use '' if don't want to specify

    Returns
    -------
    None

    Examples
    --------
    >>> grant_external_access("client002", "172.25.0.2", "udp", "47.254.124.205", "2222")
    >>> grant_external_access("client002", "172.25.0.2", "udp", dst_port="")

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == "":
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_ip, str):
        raise TypeError("dst_ip is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")
    # if dst_ip_port is not None and \
    # not (isinstance(dst_ip_port, List) and len(dst_ip_port) == 2 and all(isinstance(item, str) for item in dst_ip_port)):
    #     raise TypeError("dst_ip_port is expected to be a two element str list")

    # cip = get_container_ip(container_name)
    cip = container_ip

    # manipulate the iptables
    cmd = "sudo iptables -I "
    # define the spec, container_name here is the chain name
    spec = container_name + "-extn" + " -i docker1 "
    if protocol != "":
        spec = spec + "-p " + protocol + " "
    spec = spec + "-s " + cip + " "
    if dst_ip != "":
        spec += "-d " + dst_ip + " "
    if dst_port != "":
        spec += "--dport " + dst_port + " "
    # if dst_ip_port is not None:
    #     if dst_ip_port[0] is not '':
    #         spec = spec + "-d " + dst_ip_port[0] + " "
    #     if dst_ip_port[1] is not '':
    #         spec = spec + "--dport " + dst_ip_port[1]+ " "
    spec = spec + "-j ACCEPT"

    cmd += spec
    subprocess.run(split(cmd))


def grant_host_access(
    container_name: str, container_ip: str, protocol: str = "", dst_port: str = ""
):
    """
    Grant the target container access to local host

    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    container_ip
        ip addr of the container i.e. returned by app_management.get_container_ip
    protocol: optional
        access protocol, could be either tcp or udp
    dst_port: optional
        destination port on the local host

    Returns
    -------
    None

    Examples
    --------
    >>> grant_host_access("client003", "172.25.0.2", "udp", "2222")

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == "":
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    # cip = get_container_ip(container_name)
    cip = container_ip

    # manipulate the iptables
    cmd = "sudo iptables -I "
    # specify the spec
    spec = container_name + "-host" + " -i docker1 "
    if protocol != "":
        spec = spec + "-p " + protocol + " "
    spec = spec + "-s " + cip + " "
    if dst_port != "":
        spec = spec + "--dport " + dst_port + " "
    spec = spec + "-j ACCEPT"

    cmd += spec
    subprocess.run(split(cmd))


def revoke_all_access(container_name: str, option: int = 0):
    """
    Revoke all accesses granted to a particular container
    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    option: optional
        0, flush both external and host access
        1, flush all external accesses
        2, flush all host accesses
    Returns
    -------
    None

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    if not isinstance(option, int):
        raise TypeError("option is expected to be str")

    if option == 0:
        cmd = "sudo iptables -F " + container_name + "-extn"
        subprocess.run(split(cmd))
        cmd = "sudo iptables -F " + container_name + "-host"
        subprocess.run(split(cmd))
    elif option == 1:
        cmd = "sudo iptables -F " + container_name + "-extn"
        subprocess.run(split(cmd))
    elif option == 2:
        cmd = "sudo iptables -F " + container_name + "-host"
        subprocess.run(split(cmd))


def revoke_external_access(
    container_name: str,
    container_ip: str,
    protocol: str = "",
    dst_ip: str = "",
    dst_port: str = "",
) -> None:
    """
    Revoke the target container access to external host

    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    container_ip
        ip addr of the container i.e. returned by app_management.get_container_ip
    protocol: optional
        access protocol, could be either tcp or udp
    dst_ip: optional
        destination ip address, use '' if don't want to specify
    dst_port: optional
        destination port, use '' if don't want to specify

    Returns
    -------
    None

    Examples
    --------
    >>> revoke_external_access("client002", "172.25.0.2", "udp", "47.254.124.205", "2222")
    >>> revoke_external_access("client002", "172.25.0.2", "udp", dst_port="2222"])

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == "":
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_ip, str):
        raise TypeError("dst_ip is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")
    # if dst_ip_port is not None and not (isinstance(dst_ip_port, List) and len(dst_ip_port) == 2 and all(
    #         isinstance(item, str) for item in dst_ip_port)):
    #     raise TypeError("dst_ip_port is expected to be a two element str list")

    # cip = get_container_ip(container_name)
    cip = container_ip

    # manipulate the iptables
    cmd = "sudo iptables -D "
    # define the spec
    spec = container_name + "-extn" + " -i docker1 "
    if protocol != "":
        spec = spec + "-p " + protocol + " "
    spec = spec + "-s " + cip + " "
    if dst_ip != "":
        spec += "-d " + dst_ip + " "
    if dst_port != "":
        spec += "--dport " + dst_port + " "
    # if dst_ip_port is not None:
    #     if dst_ip_port[0] is not '':
    #         spec = spec + "-d " + dst_ip_port[0] + " "
    #     if dst_ip_port[1] is not '':
    #         spec = spec + "--dport " + dst_ip_port[1] + " "
    spec = spec + "-j ACCEPT"

    cmd += spec
    subprocess.run(split(cmd))


def revoke_host_access(
    container_name: str, container_ip: str, protocol: str = "", dst_port: str = ""
):
    """
    Revoke the target container access to local host

    Parameters
    ----------
    container_name
        name of the container i.e. returned by app_management.spawn_app
    container_ip
        ip addr of the container i.e. returned by app_management.get_container_ip
    protocol: optional
        access protocol, could be either tcp or udp
    dst_port: optional
        destination port on the local host

    Returns
    -------
    None

    Examples
    --------
    >>> revoke_host_access("client003", "172.25.0.2", "udp", "2222")

    """
    # argument check
    if not isinstance(container_name, str):
        raise TypeError("container_name is expected to be str")
    elif container_name == "":
        raise ValueError("container_name is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == "":
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    # cip = get_container_ip(container_name)
    cip = container_ip

    # manipulate the iptables
    cmd = "sudo iptables -D "
    # specify the spec
    spec = container_name + "-host" + " -i docker1 "
    if protocol != "":
        spec = spec + "-p " + protocol + " "
    spec = spec + "-s " + cip + " "
    if dst_port != "":
        spec = spec + "--dport " + dst_port + " "
    spec = spec + "-j ACCEPT"

    cmd += spec
    subprocess.run(split(cmd))
