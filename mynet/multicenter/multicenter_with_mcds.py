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
        self.adjacency = {}
        self.positions, _ = generate_connected_udg(
            n=ap_number,
            signal_range=signal_range,
            seed=int(time.time())
        )
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)


        self.ap_links = [] # [{ src_dpid: "", dst_dpid: "", port: int}]
        self.center_dpids = []
        self.aps = {}
        self.hosts = {}
        self.controller = RemoteController("c0", ip="127.0.0.1", port=6654)
    
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
            ap_position = self.positions[dpid]
            position_x = ap_position[0]
            position_y = ap_position[1]
            position_z = 0
            position = f"{position_x},{position_y},{position_z}"

            dpid, _ = self.add_ap(wlans=3, position=position)

            host = self.add_host(dpid)
            self.hosts[dpid] = host


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
            self.port_to_mesh[local_intf] = local_mesh_ssid

            adj_list = self.adjacency[dpid]
            for adj_dpid in adj_list:
                if adj_dpid not in self.center_dpids and added_links[adj_dpid]:
                    local_ap = self.aps[adj_dpid]
                    local_intf = f"{local_ap.name}-wlan3"
                    self.net.addLink(local_ap, intf=local_intf, cls=mesh, ssid=local_mesh_ssid, channel=8)
                    self.port_to_mesh[local_intf] = local_mesh_ssid
                    self.net.addLink(self.hosts[adj_dpid], local_ap)
                    added_links[adj_dpid] = 0

            center_intf = f"{center_ap.name}-wlan2"
            info(f"Add center link: {center_intf}\n")
            self.net.addLink(self.hosts[dpid], center_ap)
            self.net.addLink(center_ap, intf=center_intf, cls=mesh, ssid="mesh-center", channel=5)
            self.port_to_mesh[center_intf] = "mesh-center"

    def get_ap_list(self):
        return list(self.aps.values())

    def get_host_list(self):
        return list(self.hosts.values())

    def make_ap_links(self):
            # for k, vs in self.adjacency.items():
        for k, vs in self.adjacency.items():
            new_k = int(k, 16)
            new_vs = [ int(v, 16) for v in vs ]
            links = []
            if k in self.center_dpids:
                for v in vs:
                    new_v = int(v, 16)
                    if v in self.center_dpids:
                        link = {"src_dpid": str(new_k), "dst_dpid": str(new_v), "port_no": 2}
                    else:
                        link = {"src_dpid": str(new_k), "dst_dpid": str(new_v), "port_no": 3}
                    links.append(link)
            else:
                find_center_flag = False
                for v in vs:
                    new_v = int(v, 16)
                    if v in self.center_dpids and find_center_flag:
                        continue
                    if v in self.center_dpids:
                        find_center_flag = True
                    link = {"src_dpid": str(new_k), "dst_dpid": str(new_v), "port_no": 3}
                    links.append(link)
            self.ap_links = self.ap_links + links

    def config(self):
        info("Get init center dpids.......\n")
        self._get_center_dpids()
        info(self.center_dpids)
        info("\n")
        info("Get adjacency.......\n")
        info(self.adjacency)
        info("\n")
        info("Make ap links.......\n")
        self.make_ap_links()
        info(self.ap_links)
        info("\n")

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
