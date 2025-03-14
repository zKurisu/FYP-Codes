import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc

def run(apName, portName):
    with grpc.insecure_channel("localhost:10086") as channel:
        stub = apcontrol_pb2_grpc.APControlStub(channel)
        response = stub.APConnectMesh(apcontrol_pb2.APInfoRequest(apName=apName, portName=portName))
        print(f"Ryu send apName: {apName} to Mininet Server")
        status = response.status
        print(f"Mininet Server connect {apName} to mesh: {status}")

if __name__ == '__main__':
    run(apName="ap1", portName="ap1-mp2")
