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
    ap1 = net.addAccessPoint("ap1", wlans=2, ssid="ap1", position="20,20,0")
    ap2 = net.addAccessPoint("ap2", wlans=2, ssid="ap2", position="60,20,0")
    c0 = net.addController("c0")

    net.setPropagationModel(model="logDistance", exp=5)
    net.plotGraph(max_x=100, max_y=50)

    net.configureNodes()

    net.addLink(h1, ap1)
    net.addLink(h2, ap1)
    net.addLink(h3, ap2)
    net.addLink(h4, ap2)

    net.addLink(ap1, ap2)

    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel("info")
    mytopo(sys.argv)
