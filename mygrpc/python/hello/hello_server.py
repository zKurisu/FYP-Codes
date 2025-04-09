from concurrent import futures
import grpc

import mygrpc.python.hello.hello_pb2_grpc as hello_pb2_grpc
import mygrpc.python.hello.hello_pb2 as hello_pb2

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"Received request from {request.name}")
        return hello_pb2.HelloReply(msg=f"Hello {request.name}")

def run():
    port = "10086"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    run()
