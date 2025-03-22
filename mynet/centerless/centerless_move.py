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

class MyNet(MyNetBase):
    def __init__(self, node_num=8): ######## Specify this
        super(MyNet, self).__init__()
        self.net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
        self.aps = []
        self.hosts = []
        self.controller = self.net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6654)
        self.node_num = node_num

    def get_ap_list(self):
        return self.aps
    def get_host_list(self):
        return self.hosts
    
    def add_nodes_batch(self):
        """ A Node is [AP + Host] """
        opt_params = {}
        #opt_params['protocols']='OpenFlow13'
        opt_params['min_v'] = 0.5
        opt_params['max_v'] = 0.9

        for i in range(1, self.node_num+1):
            host_mac = next_mac("host", i)
            ap_mac = next_mac("ap", i)
            h = self.net.addHost('h%d' % i, mac=host_mac)
            info(f"*** Creating Host with MAC {host_mac} \n")
            ap = self.net.addAccessPoint('ap%d' % i, wlans=3, ssid='ssid%d' % i, mac=ap_mac, **opt_params)

            self.aps.append(ap)
            self.hosts.append(h)

    def add_links_batch(self):
        """ Link ap and host """
        if len(self.aps) != len(self.hosts):
            exit("Number of aps should be same as hosts")

        for i in range(0, len(self.aps)):
            self.net.addLink(self.aps[i], self.hosts[i])
            self.net.addLink(self.aps[i], intf=f'ap{i+1}-wlan2', cls=mesh, ssid='mesh-ssid1', channel=5)
            self.port_to_mesh[f'ap{i+1}-wlan2'] = 'mesh-ssid1'

    def start_aps(self):
        for ap in self.aps:
            ap.start([self.controller])

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

    def cli(self):
        info("*** Running CLI\n")
        CLI(self.net)

    def stop(self):
        info("*** Stopping network\n")
        self.net.stop()
