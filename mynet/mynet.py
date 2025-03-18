#!/usr/bin/env python
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController

class MyNetBase():
    def __init__(self):
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

        self.aps = {}
        self.hosts = {}
        self.controller = RemoteController("c0", ip="127.0.0.1", port=6654)
    
    def start_aps(self):
        for dpid in self.aps.keys():
            self.aps[dpid].start([self.controller])

    def add_links(self):
        pass

    def get_ap_list(self):
        return list(self.aps.values())

    def get_host_list(self):
        return list(self.hosts.values())

    def config(self):
        pass
    
    def start(self):
        info("Start Net.......\n")
        self.net.build()
        self.controller.start()
        self.start_aps()
    
    def stop(self):
        self.net.stop()

    def cli(self):
        CLI(self.net)

    def run(self):
        self.config()
        self.start()
        self.cli()
        self.stop()
