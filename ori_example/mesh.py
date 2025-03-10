#!/usr/bin/env python

"""
This example shows on how to enable the mesh mode
The wireless mesh network is based on IEEE 802.11s
"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

def add_station_batch(net, number):
    info("*** Creating nodes\n")
    stas = []

    for i in range(1, number+1):
        station = net.addStation(f"sta{i}")
        stas.append(station)

    return stas

def add_link_batch(net, stas):
    info("*** Creating links\n")
    for i, sta in enumerate(stas, start=1):
        net.addLink(sta, cls=mesh, ssid='meshNet', intf=f'sta{i}-wlan0', channel=5, ht_cap='HT40+')  #, passwd='thisisreallysecret')

def plotGraph_resize(net, number):
    max_x = number * 20
    max_y = max_x
    net.plotGraph(max_x=max_x, max_y=max_y)
    net.setMobilityModel(time=0, model='RandomDirection',
                            max_x=max_x, max_y=max_y,
                            min_v=0.2, max_v=0.5, seed=20)

def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    number = 6

    info("*** Creating nodes\n")
    stas = add_station_batch(net, number)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Creating links\n")
    add_link_batch(net, stas)

    plotGraph_resize(net, number)

    info("*** Starting network\n")
    net.build()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
