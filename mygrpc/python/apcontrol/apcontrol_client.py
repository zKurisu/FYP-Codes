import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc
from google.protobuf import empty_pb2

def run(dpid, portName):
    with grpc.insecure_channel("localhost:10086") as channel:
        stub = apcontrol_pb2_grpc.APControlStub(channel)
        response = stub.APConnectMesh(apcontrol_pb2.APInfoRequest(dpid=dpid, portName=portName))
        print(f"Ryu send dpid: {dpid} to Mininet Server")
        status = response.status
        print(f"Mininet Server connect {dpid} to mesh: {status}")

        return status

def getAPLinks():
    try:
        with grpc.insecure_channel("localhost:10086") as channel:
            stub = apcontrol_pb2_grpc.APControlStub(channel)
            request = empty_pb2.Empty()
            response = stub.GetAPLinks(request)
            print(f"Ryu send getAPLinks request to Mininet Server")
            return response
    except grpc.RpcError as e:
        print(f"Failed to connect to gRPC server: {e}")
        # 你可以在这里返回一个默认值或重新抛出异常
        return None  # 或者 raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None  # 或者根据你的需求处理

if __name__ == '__main__':
    run(dpid="100001", portName="ap1-mp2")

