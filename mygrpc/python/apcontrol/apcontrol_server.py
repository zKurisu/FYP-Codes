from concurrent import futures
import grpc
import mygrpc.python.apcontrol.apcontrol_pb2 as apcontrol_pb2
import mygrpc.python.apcontrol.apcontrol_pb2_grpc as apcontrol_pb2_grpc

class TestAP():
    def __init__(self, dpid):
        self.dpid = dpid

class APControl(apcontrol_pb2_grpc.APControlServicer):
    def __init__(self, net):
        self.net = net
        self.aps = net.get_ap_list() # Place APs here
        self.port_to_mesh = net.port_to_mesh # Place APs here
        self.ap_links = net.ap_links
    def APConnectMesh(self, request, context):
        ... # Do AP Connect Mesh
        ... # If OK
        for ap in self.aps:
            if ap.dpid == request.dpid:
                if self.port_to_mesh.get(request.portName) != None:
                    ap.cmd(f"iw dev {request.portName} mesh join {self.port_to_mesh[request.portName]}")
                    print(f"{ap.name} Run: iw dev {request.portName} mesh join {self.port_to_mesh[request.portName]}")
                else:
                    print("No mesh ssid in port to mesh table")
        
        print(f"{request.dpid}:{request.portName} connect to mesh successfully")
        return apcontrol_pb2.APInfoReply(status="OKK")
    
    def GetAPLinks(self, request, context):
        if hasattr(self.net, "update_ap_links"):
            self.net.update_ap_links()
        print("Return links")
        # 将 APLinks 数据转换为 APLinks 消息
        ap_links_response = apcontrol_pb2.APLinksResponse()
        for ap_link in self.ap_links:
            ap_links_response.ap_links.append(
                apcontrol_pb2.APLinks(
                    src_dpid=ap_link["src_dpid"],
                    dst_dpid=ap_link["dst_dpid"],
                    port_no=ap_link["port_no"]
                )
            )

        return ap_links_response

class APCrpcserver():
    def __init__(self, net):
        self.port = "10086"
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        apcontrol_pb2_grpc.add_APControlServicer_to_server(APControl(net), self.server)
        self.server.add_insecure_port("[::]:" + self.port)

    def run(self):
        print(f"Start RPC Server at {self.port}")
        self.server.start()
        self.server.wait_for_termination()

    def stop(self):
        self.server.stop(0)

# if __name__ == '__main__':
#     ap1 = TestAP("100001")
#     ap2 = TestAP("100002")
#     run([ap1, ap2])

