import grpc

# import the generated classes
from . import iptables_manager_pb2_grpc
from . import iptables_manager_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = iptables_manager_pb2_grpc.IptablesManagerStub(channel)


def create_chain(container_id: str) -> int:
    """
    Create iptables chains with the same name as the container name into DOCKER-USER chain and INPUT chain

    Parameters
    ----------
    container_id
        name of the container i.e. returned by app_management.spawn_app

    Returns
    -------
    Status of request: 1 -> success, -1 -> TypeError

    """
    # argument check
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")

    cname = iptables_manager_pb2.Cname(container_name=container_id)
    res = stub.CreateChain(cname)
    return res


def delete_chain(container_id: str) -> int:
    # argument check
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")

    cname = iptables_manager_pb2.Cname(container_name=container_id)
    res = stub.DeleteChain(cname)
    return res


def grant_external_access(container_id: str, container_ip: str, protocol: str = '', dst_ip: str = '',
                          dst_port: str = '') -> int:
    """
    Grant the target container access to external host

    Parameters
    ----------
    container_id
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
    Status of request: 1 -> success, -1 -> TypeError

    Examples
    --------
    >>> grant_external_access("client002", "172.25.0.2", "udp", "47.254.124.205", "2222")
    >>> grant_external_access("client002", "172.25.0.2", "udp", dst_port="")

    """
    # argument check
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == '':
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_ip, str):
        raise TypeError("dst_ip is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    request = iptables_manager_pb2.ExternalAccessRequest(container_name=container_id, container_ip=container_ip, protocol=protocol, dst_ip=dst_ip, dst_port=dst_port)
    res = stub.GrantExternalAccess(request)
    return res

def grant_host_access(container_id: str, container_ip: str, protocol: str = '', dst_port: str = ''):
    """
    Grant the target container access to local host

    Parameters
    ----------
    container_id
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
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == '':
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    request = iptables_manager_pb2.HostAccessRequest(container_name=container_id, container_ip=container_ip, protocol=protocol, dst_port=dst_port)
    res = stub.GrantHostAccess(request)
    return res


def revoke_all_access(container_id: str, option: int=0):
    """
    Revoke all accesses granted to a particular container
    Parameters
    ----------
    container_id
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
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")
    if not isinstance(option, int):
        raise TypeError("option is expected to be str")

    cname = iptables_manager_pb2.RevokeAllRequest(container_name=container_id)
    res = stub.RevokeAllAccess(cname)
    return res


def revoke_external_access(container_id: str, container_ip: str, protocol: str = '', dst_ip: str = '',
                           dst_port: str = '') -> None:
    """
    Revoke the target container access to external host

    Parameters
    ----------
    container_id
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
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == '':
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_ip, str):
        raise TypeError("dst_ip is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    request = iptables_manager_pb2.ExternalAccessRequest(container_name=container_id, container_ip=container_ip, protocol=protocol, dst_ip=dst_ip, dst_port=dst_port)
    res = stub.RevokeExternalAccess(request)
    return res


def revoke_host_access(container_id: str, container_ip: str, protocol: str = '', dst_port: str = ''):
    """
    Revoke the target container access to local host

    Parameters
    ----------
    container_id
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
    if not isinstance(container_id, str):
        raise TypeError("container_id is expected to be str")
    elif container_id == '':
        raise ValueError("container_id is expected to be non empty")
    if not isinstance(container_ip, str):
        raise TypeError("container_ip is expected to be str")
    elif container_ip == '':
        raise ValueError("container_ip is expected to be non empty")
    if not isinstance(protocol, str):
        raise TypeError("protocol is expected to be str")
    if not isinstance(dst_port, str):
        raise TypeError("dst_port is expected to be str")

    request = iptables_manager_pb2.HostAccessRequest(container_name=container_id, container_ip=container_ip, protocol=protocol, dst_port=dst_port)
    res = stub.RevokeHostAccess(request)
    return res
