"""
所有节点间都能通信
"""

from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI

from mininet.log import info, setLogLevel
import sys

def mytopo(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    h1 = net.addHost("h1", mac="00:00:00:00:00:11")
    h2 = net.addHost("h2", mac="00:00:00:00:00:12")
    h3 = net.addHost("h3", mac="00:00:00:00:00:21")
    h4 = net.addHost("h4", mac="00:00:00:00:00:22")
    h5 = net.addHost("h5", mac="00:00:00:00:00:31")
    h6 = net.addHost("h6", mac="00:00:00:00:00:32")
    ap1 = net.addAccessPoint("ap1", wlans=2, ssid="ap1", position="20,20,0")
    ap2 = net.addAccessPoint("ap2", wlans=2, ssid="ap2", position="52,20,0")
    ap3 = net.addAccessPoint("ap3", wlans=2, ssid="ap3", position="100,20,0")
    c0 = net.addController("c0")

    net.setPropagationModel(model="logDistance", exp=5)

    net.configureNodes()
    net.plotGraph(max_x=120, max_y=50)

    net.addLink(h1, ap1)
    net.addLink(h2, ap1)
    net.addLink(h3, ap2)
    net.addLink(h4, ap2)
    net.addLink(h5, ap3)
    net.addLink(h6, ap3)

    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel("info")
    mytopo(sys.argv)
