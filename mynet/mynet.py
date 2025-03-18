#!/usr/bin/env python
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController

class MyNetBase():
    def __init__(self):
        setLogLevel("info")
        info("Create net...\n")
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

        self.aps = {}
        self.hosts = {}
        info("Connect controller...\n")
        self.controller = RemoteController("c0", ip="127.0.0.1", port=6654)
        self.net.addController(self.controller)
    
    def get_ap_list(self): ######### Define this in child
        return list(self.aps.values())

    def get_host_list(self): ######### Define this in child
        return list(self.hosts.values())

    def config(self): ######### Define this in child, add nodes, set mode, configure node, add links
        pass
    
    def start_aps(self): ######### Define this in child
        for dpid in self.aps.keys():
            self.aps[dpid].start([self.controller])

    def start(self):
        info("Start Net.......\n")
        self.net.build()
        self.controller.start()
        self.start_aps()
    
    def cli(self):
        info("CLI Start...\n")
        CLI(self.net)
    
    def stop(self):
        info("Net stop...\n")
        self.net.stop()

    def run(self):
        self.config()
        self.start()
        self.cli()
        self.stop()
    
def set_mode(conf_func):
    def wrapper(mynet):
        info("Set propagation model...\n")
        mynet.net.setPropagationModel(model="logDistance", exp=5)
        info("Set plotGraph...\n")
        mynet.net.plotGraph(max_x=150, max_y=100)
        conf_func(mynet)
    return wrapper
