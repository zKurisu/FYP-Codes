#!/usr/bin/env python
import sys
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, AP, OVSAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.wmediumdConnector import interference
from utils.next_mac import next_mac

def add_nodes_batch(net, number):
    """ A Node is [AP + Host] """
    opt_params = {}
    #opt_params['protocols']='OpenFlow13'
    opt_params['min_v'] = 0.5
    opt_params['max_v'] = 0.9

    aps = []
    hosts = []

    for i in range(1, number+1):
        host_mac = next_mac("host", i)
        ap_mac = next_mac("ap", i)
        h = net.addHost('h%d' % i, mac=host_mac)
        info(f"*** Creating Host with MAC {host_mac} \n")
        ap = net.addAccessPoint('ap%d' % i, wlans=3, ssid='ssid%d' % i, mac=ap_mac, **opt_params)

        aps.append(ap)
        hosts.append(h)

    return aps, hosts

def add_links_batch(net, aps, hosts):
    """ Link ap and host """
    if len(aps) != len(hosts):
        exit("Number of aps should be same as hosts")

    for i in range(0, len(aps)):
        net.addLink(aps[i], hosts[i])
        net.addLink(aps[i], intf=f'ap{i+1}-wlan2', cls=mesh, ssid='mesh-ssid1', channel=5)


def start_aps(aps, controllers):
    for ap in aps:
        ap.start(controllers)

def topology(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    info("*** Creating nodes\n")

    aps, hosts = add_nodes_batch(net, 8)
    
    # c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6654)
    c1 = net.addController('c1')
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=5)
    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=100, max_y=100, seed=20)
    info("*** Configuring wifi nodes\n")
    net.configureNodes()
    info("*** Associating and Creating Links\n")

    add_links_batch(net, aps, hosts)

    net.plotGraph(max_x=100, max_y=100)
    info("*** Starting network\n")
    net.build()
    c1.start()

    start_aps(aps, [c1])

    info("*** Running CLI\n")
    CLI(net)
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
