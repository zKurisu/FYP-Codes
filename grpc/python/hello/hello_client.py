import grpc
import hello_pb2
import hello_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:10086") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        print("Before call:")
        response = stub.SayHello(hello_pb2.HelloRequest(name="Orkarin"))
        print("After call:")
        print("Client receivee: ", response.msg)

if __name__ == '__main__':
    print("Client run...")
    run()
