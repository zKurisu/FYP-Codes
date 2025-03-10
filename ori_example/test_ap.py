from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd, mesh
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

def topology():
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("****** Add ap")
    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1', position='10,10,0')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid2', position='90,10,0')
    c0 = net.addController('c0')

    info("****** Configuring nodes\n")
    net.configureNodes()

    net.plotGraph(max_x=100, max_y=100)

    info("****** Configuring link\n")
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5, ip='10.0.0.1/24')
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5, ip='10.0.0.2/24')

    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    info("***** Running CLI\n")
    CLI(net)

    info("***** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

