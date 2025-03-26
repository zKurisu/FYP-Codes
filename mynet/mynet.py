#!/usr/bin/env python
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from utils.next_mac import next_mac

class MyNetBase():
    def __init__(self):
        setLogLevel("info")
        info("Create net...\n")
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

        self.aps = {} ##### Add ap in this way
        self.hosts = {} ##### Add host in this way
        self.port_to_mesh = {} ##### Port to mesh ssid table
        info("Connect controller...\n")
        self.controller = RemoteController("c0", ip="127.0.0.1", port=6654)
        self.net.addController(self.controller)
        self.signal_range = 31.484254489723796
    
    def get_ap_list(self):
        return list(self.aps.values())

    def get_host_list(self):
        dpids = list(self.hosts.keys())
        if len(dpids) != 0:
            first_dpid = dpids[0]
            t = type(self.hosts[first_dpid])
            if t.__name__ == "list":
                host_list = []
                for dpid in dpids:
                    host_list = host_list + self.hosts[dpid]
                return host_list
            else:
                return list(self.hosts.values())
        return []

    def get_next_apName(self):
        if type(self.aps).__name__ == "list":
            return f"{len(self.aps) + 1}"
        return f"ap{len(self.aps.keys()) + 1}" # No ap0

    def get_next_dpid(self):
        if type(self.aps).__name__ == "list":
            return str(10**15 + len(self.aps) + 1)
        return hex(0x10**15 + len(self.aps.keys()) + 1)[2:] # No ap0
    
    def get_next_hostName(self):
        return f"h{len(self.get_host_list()) + 1}" # No h0

    def add_ap(self, **kwargs):
        apName = self.get_next_apName()
        dpid = self.get_next_dpid()
        if type(self.aps).__name__ == "list":
            index = len(self.aps) + 1
        else:
            index = len(self.aps.keys()) + 1
        mac = next_mac("ap", index)
        ap = self.net.addAccessPoint(
                apName,
                dpid=dpid,
                mac=mac,
                **kwargs)
        self.aps[dpid] = ap
        return dpid, ap
    
    def add_host(self, dpid):
        hostName = self.get_next_hostName()
        index = len(self.get_host_list()) + 1
        mac = next_mac("host", index)
        host = self.net.addHost(
                hostName,
                mac=mac)
        self.hosts.setdefault(dpid, [])
        self.hosts[dpid].append(host)
        return host

    def add_hosts(self, dpid, hosts):
        self.hosts[dpid] = hosts

    def config(self): ######### Define this in child, add nodes, configure node, add links
        pass
    
    def start_aps(self):
        info("Start aps.......\n")
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
        info("Net run...\n")
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
