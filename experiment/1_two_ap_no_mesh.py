"""
若两 AP 没有以 mesh 方式连接, 就算信号覆盖, 也无法通信. 信号不覆盖自然也不能通信
"""

from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.cli import CLI

from mininet.log import setLogLevel, info
import sys

def mytopo(args):
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    info("Create Mininet_wifi network OK...\n")

    h1 = net.addHost('h1', mac='00:00:00:00:00:11')
    h2 = net.addHost('h2', mac='00:00:00:00:00:12')
    h3 = net.addHost('h3', mac='00:00:00:00:00:21')
    h4 = net.addHost('h4', mac='00:00:00:00:00:22')

    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ap1', position='10,10,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ap2', position='60,10,0')
    c0 = net.addController('c0')
    info("Add nodes to network OK...\n")

    net.configureNodes()
    info("configureNodes OK...\n")

    net.plotGraph(max_x=100, max_y=50)
    info("Plot OK...\n")

    net.addLink(h1, ap1)
    net.addLink(h2, ap1)
    net.addLink(h3, ap2)
    net.addLink(h4, ap2)
    info("Add link OK...\n")
    
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    info("Start Network OK...\n")

    CLI(net)
    info("Enter CLI OK...\n")

    net.stop()
    info("Stop network OK...\n")
    
if __name__ == '__main__':
    setLogLevel("info")
    info("Set log level to info\n")
    mytopo(sys.argv)
