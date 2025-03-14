from mygrpc.python.apcontrol.apcontrol_server import run as rpcServerRun

class MyAP():
    def __init__(self, name):
        self.name = name

ap1 = MyAP("ap1")
ap2 = MyAP("ap2")

rpcServerRun([ap1, ap2])
