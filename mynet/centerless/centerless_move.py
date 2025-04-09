#!/usr/bin/env python
from mynet.mynet import MyNetBase, set_move_mode
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd, mesh, adhoc
from utils.find_MCDS import get_adjacency

class MyNet(MyNetBase):
    def __init__(self, ap_number=8): ######## Specify this
        super(MyNet, self).__init__()
        self.node_num = ap_number
        self.ap_links = []

    def _get_adjacency(self):
        self.adjs = {}
        self.nodes_dict = {}
        for dpid in self.aps.keys():
            int_dpid = str(int(dpid, 16))
            x, y, _ = self.aps[dpid].position
            self.nodes_dict[int_dpid] = (x, y)

        self.adjs = get_adjacency(nodes_dict=self.nodes_dict, signal_range=self.signal_range)

    def update_ap_links(self):
        self.ap_links = []
        self._get_adjacency()
        for k, vs in self.adjs.items():
            links = [{"src_dpid": k, "dst_dpid": v, "port_no": 2} for v in vs ]
            self.ap_links = self.ap_links + links
    
    def add_nodes_batch(self):
        """ A Node is [AP + Host] """
        opt_params = {}
        #opt_params['protocols']='OpenFlow13'
        opt_params['min_v'] = 0.1
        opt_params['max_v'] = 0.5

        for _ in range(1, self.node_num+1):
            dpid, _ = self.add_ap(wlans=3, **opt_params)
            self.add_host(dpid)

    def add_links_batch(self):
        """ Link ap and host """
        for dpid in self.aps.keys():
            self.net.addLink(self.aps[dpid], self.hosts[dpid][0])
            self.net.addLink(self.aps[dpid], intf=f'{self.aps[dpid].name}-wlan2', cls=mesh, ssid='mesh-centerless', channel=5)
            self.port_to_mesh[f'{self.aps[dpid].name}-wlan2'] = 'mesh-centerless'

    @set_move_mode
    def config(self):
        info("--- Change")
        info("*** Creating nodes\n")
        self.add_nodes_batch()
        
        info("*** Configuring wifi nodes\n")
        self.net.configureNodes()
        info("*** Associating and Creating Links\n")

        self.add_links_batch()

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
