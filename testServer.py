from mygrpc.python.apcontrol.apcontrol_server import run as rpcServerRun

class MyAP():
    def __init__(self, dpid):
        self.dpid = dpid

ap1 = MyAP("100001")
ap2 = MyAP("100002")

rpcServerRun([ap1, ap2])
