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
        dpid = self.get_next_dpid()
        ap1 = self.net.addAccessPoint("ap1", dpid=dpid, wlans=2, ssid="ap1", position="20,20,0", mac="02:00:00:00:00:01")
        self.add_ap(dpid, ap1)
        h1 = self.net.addHost("h1", mac="00:00:00:00:00:11")
        h2 = self.net.addHost("h2", mac="00:00:00:00:00:12")
        self.add_hosts(dpid, [h1, h2])

        dpid = self.get_next_dpid()
        ap2 = self.net.addAccessPoint("ap2", wlans=2, ssid="ap2", position="52,20,0", mac="02:00:00:00:00:02")
        self.add_ap(dpid, ap2)
        h3 = self.net.addHost("h3", mac="00:00:00:00:00:21")
        h4 = self.net.addHost("h4", mac="00:00:00:00:00:22")
        self.add_hosts(dpid, [h3, h4])

        dpid = self.get_next_dpid()
        ap3 = self.net.addAccessPoint("ap3", wlans=2, ssid="ap3", position="100,20,0", mac="02:00:00:00:00:03")
        self.add_ap(dpid, ap3)
        h5 = self.net.addHost("h5", mac="00:00:00:00:00:31")
        h6 = self.net.addHost("h6", mac="00:00:00:00:00:32")
        self.add_hosts(dpid, [h5, h6])

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
