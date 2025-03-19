from concurrent import futures
import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc

class TestAP():
    def __init__(self, dpid):
        self.dpid = dpid

class APControl(apcontrol_pb2_grpc.APControlServicer):
    def __init__(self, aps, port_to_mesh):
        self.aps = aps # Place APs here
        self.port_to_mesh = port_to_mesh # Place APs here
    def APConnectMesh(self, request, context):
        ... # Do AP Connect Mesh
        ... # If OK
        for ap in self.aps:
            if ap.dpid == request.dpid:
                ap.cmd(f"iw dev {request.portName} mesh join {self.port_to_mesh[request.portName]}")
                print(f"{ap.name} Run: iw dev {request.portName} mesh join {self.port_to_mesh[request.portName]}")
        
        print(f"{request.dpid}:{request.portName} connect to mesh successfully")
        return apcontrol_pb2.APInfoReply(status="OKK")

def run(aps, port_to_mesh):
    port = "10086"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apcontrol_pb2_grpc.add_APControlServicer_to_server(APControl(aps, port_to_mesh), server)
    server.add_insecure_port("[::]:" + port)
    print(f"Start RPC Server at {port}")
    server.start()
    server.wait_for_termination()

# if __name__ == '__main__':
#     ap1 = TestAP("100001")
#     ap2 = TestAP("100002")
#     run([ap1, ap2])
