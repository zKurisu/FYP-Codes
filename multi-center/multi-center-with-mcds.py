#!/usr/bin/env python
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller

from mcds.gen_UDG import generate_connected_udg
import requests
import json
import time

def next_mac(type, index):
    """ All MAC for AP or Host """
    if type == "host":
        prefix = 0x00
    else:
        prefix = 0x02
    return '%02x:%02x:%02x:%02x:%02x:%02x' % (
        prefix,
        (index >> 32) & 0xff,
        (index >> 24) & 0xff,
        (index >> 16) & 0xff,
        (index >> 8) & 0xff,
        index & 0xff,
    )

class MyNet():
    def __init__(self, ap_number=10, signal_range=31.484254489723796):
        self.signal_range = signal_range
        self.ap_number = ap_number
        self.adjacency = {}
        self.positions, _ = generate_connected_udg(
            n=ap_number,
            signal_range=signal_range,
            seed=int(time.time())
        )
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)


        self.center_dpids = []
        self.aps = {}
        self.hosts = {}
        self.controller = Controller("c0")
    
    def _get_center_dpids(self):
        url = "http://127.0.0.1:8000/find_center"
        try:
            data = {
                "positions": self.positions,
                "signal_range": self.signal_range
            }
            json_data = json.dumps(data)
            response = requests.post(url, json_data)
            response.raise_for_status()  # 如果状态码不是 200，抛出异常
            self.center_dpids = response.json()["center_dpids"]
            self.adjacency = response.json()["adjacency"]
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

    def add_aps(self):
        #         ap1 = self.net.addAccessPoint("ap1")
        #         self.aps["1"](ap1)
        # 
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

            ap = self.net.addAccessPoint(ap_name, dpid=dpid_str, wlans=3, position=position, mac=ap_mac)
            self.aps[dpid_str] = ap

            ap_mac = next_mac("host", ap_count+1)
            host_count = ap_count
            host_name = "h%d" % host_count
            host = self.net.addHost(host_name)
            self.hosts[dpid_str] = host

    def start_aps(self):
        for dpid in self.aps.keys():
            self.aps[dpid].start([self.controller])

    def add_links(self):
        # pass
        added_links = {}
        for dpid in self.aps.keys():
            added_links[dpid] = 1

        for dpid in self.center_dpids:
            center_ap = self.aps[dpid]
            local_mesh_ssid = f"mesh-{center_ap.name}"
            local_intf = f"{center_ap.name}-wlan3"
            self.net.addLink(center_ap, intf=local_intf, cls=mesh, ssid=local_mesh_ssid, channel=8)

            adj_list = self.adjacency[dpid]
            for adj_dpid in adj_list:
                if adj_dpid not in self.center_dpids and added_links[adj_dpid]:
                    local_ap = self.aps[adj_dpid]
                    local_intf = f"{local_ap.name}-wlan3"
                    self.net.addLink(local_ap, intf=local_intf, cls=mesh, ssid=local_mesh_ssid, channel=8)
                    self.net.addLink(self.hosts[adj_dpid], local_ap)
                    added_links[adj_dpid] = 0

            center_intf = f"{center_ap.name}-wlan2"
            info(f"Add center link: {center_intf}\n")
            self.net.addLink(self.hosts[dpid], center_ap)
            self.net.addLink(center_ap, intf=center_intf, cls=mesh, ssid="mesh-center", channel=5)

    def run(self):
        info("Get init center dpids.......\n")
        self._get_center_dpids()
        info(self.center_dpids)
        info("\n")
        info("Get adjacency.......\n")
        info(self.adjacency)

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

        info("Start Net.......\n")
        self.net.build()
        self.controller.start()
        self.start_aps()

        CLI(self.net)
        self.net.stop()
        pass


if __name__ == "__main__":
    setLogLevel("info")
    myNet = MyNet()
    myNet.run()
