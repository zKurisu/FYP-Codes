#!/usr/bin/env python
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController

from mynet.mynet import MyNetBase
from utils.gen_UDG import generate_connected_udg
from utils.next_mac import next_mac
import requests
import json
import time

class MyNet(MyNetBase):
    def __init__(self, ap_number=10, signal_range=31.484254489723796):
        super(MyNet, self).__init__()
        self.signal_range = signal_range
        self.ap_number = ap_number
        self.positions, self.adjs = generate_connected_udg(
            n=ap_number,
            signal_range=signal_range,
            seed=int(time.time())
        )
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

        self.ap_links = [] # [{ src_dpid: "", dst_dpid: "", port: int}]
        self.aps = {}
        self.hosts = {}
        self.controller = RemoteController("c0", ip="127.0.0.1", port=6654)
    
    def add_aps(self):
        for dpid in self.positions.keys():
            dpid_str = str(dpid)
            ap_count = len(self.aps)
            ap_name = "ap%d" % (ap_count+1)
            ap_position = self.positions[dpid]
            position_x = ap_position[0]
            position_y = ap_position[1]
            position_z = 0
            position = f"{position_x},{position_y},{position_z}"
            ap_mac = next_mac("ap", ap_count+1)

            ap = self.net.addAccessPoint(ap_name, dpid=dpid_str, wlans=2, position=position, mac=ap_mac)
            self.aps[dpid_str] = ap

            ap_mac = next_mac("host", ap_count+1)
            host_count = ap_count+1
            host_name = "h%d" % host_count
            host = self.net.addHost(host_name)
            self.hosts[dpid_str] = host

    def start_aps(self):
        for dpid in self.aps.keys():
            self.aps[dpid].start([self.controller])

    def add_links(self):
        for dpid in self.aps.keys():
            ap = self.aps[dpid]
            mesh_ssid = f"mesh-centerless"
            mesh_intf = f"{ap.name}-wlan2"
            self.net.addLink(ap, intf=mesh_intf, cls=mesh, ssid=mesh_ssid, channel=8)
            self.port_to_mesh[mesh_intf] = mesh_ssid
            self.net.addLink(self.hosts[dpid], ap)


    def get_ap_list(self):
        return list(self.aps.values())

    def get_host_list(self):
        return list(self.hosts.values())

    def config(self):
        info(self.adjs)
        info("\n")
        info("Add aps.......\n")
        self.add_aps()
        self.net.addController(self.controller)

        info("Set PropagationModel.......\n")
        self.net.setPropagationModel(model="logDistance", exp=5)
        self.net.plotGraph(max_x=100, max_y=100)

        info("Configure Nodes.......\n")
        self.net.configureNodes()

        info("Add Links.......\n")
        self.add_links()
    
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
