from mn_wifi.net import Mininet_wifi
from mininet.log import setLogLevel
from mn_wifi.cli import CLI

def topology():
    net = Mininet_wifi()

    print("Creating nodes")
    sta1 = net.addStation('sta1')
    sta2 = net.addStation('sta2')
    ap1 = net.addAccessPoint('ap1', ssid='mesh-ssid', mode='g', channel='1', position='50,50,0')
    ap2 = net.addAccessPoint('ap2', ssid='mesh-ssid', mode='g', channel='1', position='150,50,0')

    print("Configuring mesh network")
    net.configureNodes()

    print("Starting network")
    net.build()
    net.start()

    print("Running CLI")
    CLI(net)

    print("Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
