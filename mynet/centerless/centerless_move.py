#!/usr/bin/env python
import sys
from mynet.mynet import MyNetBase
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.wmediumdConnector import interference
from utils.next_mac import next_mac
from utils.find_MCDS import get_adjacency

class MyNet(MyNetBase):
    def __init__(self, ap_number=8): ######## Specify this
        super(MyNet, self).__init__()
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
        self.controller = self.net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6654)
        self.node_num = ap_number
        self.ap_links = []

    def _get_adjacency(self):
        self.nodes_dict = {}
        for dpid in self.aps.keys():
            x, y, _ = self.aps[dpid].position
            self.nodes_dict[dpid] = (x, y)

        self.adjs = get_adjacency(nodes_dict=self.nodes_dict, signal_range=self.signal_range)

    def update_ap_links(self):
        self._get_adjacency()
        print(self.adjs)
        for k, vs in self.adjs.items():
            links = [{"src_dpid": k, "dst_dpid": v, "port_no": 2} for v in vs ]
            self.ap_links = self.ap_links + links
    
    def add_nodes_batch(self):
        """ A Node is [AP + Host] """
        opt_params = {}
        #opt_params['protocols']='OpenFlow13'
        opt_params['min_v'] = 0.5
        opt_params['max_v'] = 0.9

        for _ in range(1, self.node_num+1):
            dpid, _ = self.add_ap(wlans=3, **opt_params)
            self.add_host(dpid)

    def add_links_batch(self):
        """ Link ap and host """
        for dpid in self.aps.keys():
            self.net.addLink(self.aps[dpid], self.hosts[dpid][0])
            self.net.addLink(self.aps[dpid], intf=f'{self.aps[dpid].name}-wlan2', cls=mesh, ssid='mesh-centerless', channel=5)
            self.port_to_mesh[f'{self.aps[dpid].name}-wlan2'] = 'mesh-centerless'

    def config(self):
        info("*** Creating nodes\n")
        self.add_nodes_batch()
        
        info("*** Configuring Propagation Model\n")
        self.net.setPropagationModel(model="logDistance", exp=5)
        self.net.setMobilityModel(time=0, model='RandomDirection',
                            max_x=100, max_y=100, seed=20)
        info("*** Configuring wifi nodes\n")
        self.net.configureNodes()
        info("*** Associating and Creating Links\n")

        self.add_links_batch()

        self.net.plotGraph(max_x=100, max_y=100)

    def start(self):
        info("*** Starting network\n")
        self.net.build()
        self.controller.start()
        self.start_aps()
        if hasattr(self, "update_ap_links"):
            print("Has method update_ap_links")
        self.update_ap_links()

    def cli(self):
        info("*** Running CLI\n")
        CLI(self.net)

    def stop(self):
        info("*** Stopping network\n")
        self.net.stop()
