import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc

def run(dpid, portName):
    with grpc.insecure_channel("localhost:10086") as channel:
        stub = apcontrol_pb2_grpc.APControlStub(channel)
        response = stub.APConnectMesh(apcontrol_pb2.APInfoRequest(dpid=dpid, portName=portName))
        print(f"Ryu send dpid: {dpid} to Mininet Server")
        status = response.status
        print(f"Mininet Server connect {dpid} to mesh: {status}")

        return status

if __name__ == '__main__':
    run(dpid="100001", portName="ap1-mp2")
