from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def mytopo():
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    sta1 = net.addStation("sta1", position="20,20,0")
    sta2 = net.addStation("sta2", position="80,20,0")
    ap1 = net.addAccessPoint("ap1", wlans=1, ssid="ap1", position="30,20,0")
    c0 = net.addController("c0")

    net.setPropagationModel(model="logDistance", exp=5)
    net.configureNodes()
    net.plotGraph(max_x=100, max_y=50)

    net.build()
    c0.start()
    ap1.start([c0])

    CLI(net)

    net.stop()

if __name__ == '__main__':
    mytopo()

