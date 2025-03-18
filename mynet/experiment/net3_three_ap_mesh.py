"""
所有节点间都能通信
"""
from mn_wifi.link import mesh
from mynet.mynet import MyNetBase, set_mode

class MyNet(MyNetBase):
    def __init__(self):
        super(MyNet, self).__init__()
    
    @set_mode
    def config(self):
        dpid, ap1 = self.add_ap(wlans=2, ssid="ap1", position="20,20,0")
        h1 = self.add_host(dpid)
        h2 = self.add_host(dpid)

        dpid, ap2 = self.add_ap(wlans=2, ssid="ap2", position="52,20,0")
        h3 = self.add_host(dpid)
        h4 = self.add_host(dpid)

        dpid, ap3 = self.add_ap(wlans=2, ssid="ap3", position="100,20,0")
        h5 = self.add_host(dpid)
        h6 = self.add_host(dpid)

        self.net.configureNodes()

        self.net.addLink(h1, ap1)
        self.net.addLink(h2, ap1)
        self.net.addLink(h3, ap2)
        self.net.addLink(h4, ap2)
        self.net.addLink(h5, ap3)
        self.net.addLink(h6, ap3)

        self.net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
        self.net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
        self.net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
