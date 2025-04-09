#!/usr/bin/env python
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

from mynet.mynet import MyNetBase, set_mode
from utils.gen_UDG import generate_connected_udg

class MyNet(MyNetBase):
    def __init__(self, ap_number=10, signal_range=31.484254489723796):
        super(MyNet, self).__init__()
        self.signal_range = signal_range
        self.ap_number = ap_number
        self.positions, self.adjs = generate_connected_udg(
            n=ap_number,
            signal_range=signal_range,
            seed=10
            # seed=int(time.time())
        )

        self.ap_links = [] # [{ src_dpid: "", dst_dpid: "", port: int}]
        self.aps = {}
        self.hosts = {}
    
    def add_aps(self):
        for dpid in self.positions.keys():
            ap_position = self.positions[dpid]
            position_x = ap_position[0]
            position_y = ap_position[1]
            position_z = 0
            position = f"{position_x},{position_y},{position_z}"

            dpid, ap = self.add_ap(wlans=2, position=position)
            self.aps[dpid] = ap

            host = self.add_host(dpid)
            self.hosts[dpid] = host

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

    def make_ap_links(self):
        for k, vs in self.adjs.items():
            links = [{"src_dpid": k, "dst_dpid": v, "port_no": 2} for v in vs ]
            self.ap_links = self.ap_links + links

    @set_mode
    def config(self):
        info(self.adjs)
        self.make_ap_links()
        info(self.ap_links)
        info("\n")
        info("Add aps.......\n")
        self.add_aps()
        self.net.addController(self.controller)

        info("Set PropagationModel.......\n")

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
