import logging
import time
from concurrent import futures

import grpc
import iptables_manager_core
import iptables_manager_pb2

# import the generated classes
import iptables_manager_pb2_grpc


class IptablesManagerServicer(iptables_manager_pb2_grpc.IptablesManagerServicer):
    def CreateChain(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        try:
            iptables_manager_core.create_chain(request.container_name)
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def DeleteChain(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        try:
            iptables_manager_core.delete_chain(request.container_name)
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def GrantExternalAccess(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        cname = request.container_name
        cip = request.container_ip
        protocol = request.protocol
        dst_ip = request.dst_ip
        dst_port = request.dst_port
        try:
            iptables_manager_core.grant_external_access(
                cname, cip, protocol, dst_ip, dst_port
            )
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def RevokeExternalAccess(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        cname = request.container_name
        cip = request.container_ip
        protocol = request.protocol
        dst_ip = request.dst_ip
        dst_port = request.dst_port
        try:
            iptables_manager_core.revoke_external_access(
                cname, cip, protocol, dst_ip, dst_port
            )
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def GrantHostAccess(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        cname = request.container_name
        cip = request.container_ip
        protocol = request.protocol
        dst_port = request.dst_port
        try:
            iptables_manager_core.grant_host_access(cname, cip, protocol, dst_port)
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def RevokeHostAccess(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        cname = request.container_name
        cip = request.container_ip
        protocol = request.protocol
        dst_port = request.dst_port
        try:
            iptables_manager_core.revoke_host_access(cname, cip, protocol, dst_port)
        except TypeError:
            print("type error")
            res.status = -1
        except Exception:
            print("something else happens")
            res.status = -2
        return res

    def RevokeAllAccess(self, request, context):
        res = iptables_manager_pb2.Response()
        res.status = 1
        try:
            iptables_manager_core.revoke_all_access(
                request.container_name, request.option
            )
        except TypeError:
            print("type error")
            res.status = -1
        # except:
        #     print("something else happens")
        #     res.status = -2
        return res


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iptables_manager_pb2_grpc.add_IptablesManagerServicer_to_server(
        IptablesManagerServicer(), server
    )
    print("Starting server. Listening on port 50051.")
    server.add_insecure_port("[::]:50051")
    server.start()
    # server.wait_for_termination()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    logging.basicConfig()
    serve()
