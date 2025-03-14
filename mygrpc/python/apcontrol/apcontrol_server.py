from concurrent import futures
import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc

class TestAP():
    def __init__(self, name):
        self.name = name

class APControl(apcontrol_pb2_grpc.APControlServicer):
    def __init__(self, aps):
        self.aps = aps # Place APs here
    def APConnectMesh(self, request, context):
        ... # Do AP Connect Mesh
        ... # If OK
        for ap in self.aps:
            if ap.name == request.apName:
                # ap.cmd(f"iw dev {request.portName} mesh join mesh-ssid")
                print(f"Run: iw dev {request.portName} mesh join mesh-ssid")
        
        print(f"{request.apName}:{request.portName} connect to mesh successfully")
        return apcontrol_pb2.APInfoReply(status="OKK")

def run(aps):
    port = "10086"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apcontrol_pb2_grpc.add_APControlServicer_to_server(APControl(aps), server)
    server.add_insecure_port("[::]:" + port)
    print(f"Start RPC Server at {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    ap1 = TestAP("ap1")
    ap2 = TestAP("ap2")
    run([ap1, ap2])
