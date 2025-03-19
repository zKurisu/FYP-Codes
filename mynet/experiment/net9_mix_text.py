### Centerless connect to ap2, mesh-ap1

from mynet.mynet import MyNetBase, set_mode

from mn_wifi.link import mesh
from mininet.log import info
from math import pi,cos,sin
from utils.next_mac import next_mac
from utils.send_apInfo import wlan_to_mesh

class MyNet(MyNetBase):
    def __init__(self):
        super(MyNet, self).__init__()
        self.aps = {}
        self.hosts = {}
        self.center_nodes = []
        self.normal_nodes_dist = {}
        self.centerless_ap = []
        self.center_number = 2 ################### Specific Part
        self.fanout = 1 ################### Specific Part
        pass

    def add_center_node(self, ap_count, center_index):
        posi_x = center_index * 30 + 50 ### Gap between Centerless
        posi_y = 40
        position = f"{posi_x},{posi_y},0"

        dpid, ap = self.add_ap(wlans=3, position=position)
        info(f"Add center ap: {dpid}\n")

        host = self.add_host(dpid)
        info(f"Add center host: {dpid}\n")

        return {
                # "ap": ap, "host": host, "hex_index": hex_index,
                "ap": ap, "host": host, 
                "position": {"x": posi_x, "y": posi_y}
                }

    # Position depends on center_position
    # Fanout depends on number specified
    # def add_normal_nodes(center, number, net):
    def add_normal_nodes(self, ap_count, center, number):
        degree_init = 90 # Position of normal node to center node
        degree_gap = 2* pi / number
        distance = 20
        center_x = center["position"]["x"]
        center_y = center["position"]["y"]

        normal_nodes = []
        for i in range(ap_count, ap_count+number):
            degree = degree_init + degree_gap * (i-1)

            posi_x = distance * cos(degree) + center_x
            posi_y = distance * sin(degree) + center_y
            
            position = f"{posi_x},{posi_y},0"

            dpid, ap = self.add_ap(wlans=2, position=position)
            info(f"Add normal ap: {dpid}\n")

            # host = net.addHost(f"normal{i}-host", mac=f"00:00:00:00:{center_hex}:{normal_hex}")
            info(f"Add normal host: {dpid}\n")
            host = self.add_host(dpid)
            normal_nodes.append({"ap": ap, "host": host, "position": position})
        return normal_nodes

    # Center and host
    # Center Mesh, name: mesh-center
    def add_center_links(self):
        for node in self.center_nodes:
            intf = f"{node["ap"].name}-wlan2"
            info(f"Add center link: {intf}\n")
            ssid = "mesh-center"
            self.net.addLink(node["host"], node["ap"])
            self.net.addLink(node["ap"], intf=intf, cls=mesh, ssid=ssid, channel=5)
            mpName = wlan_to_mesh(intf)
            self.port_to_mesh[mpName] = ssid

    # Normal and host
    # Local mesh, name: mesh-apx
    def add_normal_links(self):
        for center_node in self.center_nodes:
            center_ap_name = center_node["ap"].name
            center_intf = f"{center_ap_name}-wlan3"
            ssid = f"mesh-{center_ap_name}"
            info(f"Add normal link: {center_intf}\n")
            self.net.addLink(center_node["ap"], intf=center_intf, cls=mesh, ssid=ssid, channel=8)
            mpName = wlan_to_mesh(center_intf)
            self.port_to_mesh[mpName] = ssid

            for normal_node in self.normal_nodes_dist[center_ap_name]:
                normal_ap_name = normal_node["ap"].name
                normal_intf = f"{normal_ap_name}-wlan2"
                mpName = wlan_to_mesh(normal_intf)
                self.port_to_mesh[mpName] = ssid
                info(f"Add normal link: {normal_intf}\n")
                self.net.addLink(normal_node["host"], normal_node["ap"])
                self.net.addLink(normal_node["ap"], intf=normal_intf, cls=mesh, ssid=ssid, channel=8)

    def start_center(self):
        for node in self.center_nodes:
            node["ap"].start([self.controller])

    def start_normal(self):
        for nodes in list(self.normal_nodes_dist.values()):
            for node in nodes:
                node["ap"].start([self.controller])
    
    def start_centerless(self):
        for ap in self.centerless_ap:
            ap.start([self.controller])

    @set_mode
    def config(self):
        info("Create nodes...\n")
        dpid, apx1 = self.add_ap(wlans=2, position="60,80,0")
        hx1 = self.add_host(dpid)
        self.centerless_ap.append(apx1)

        dpid, apx2 = self.add_ap(wlans=2, position="40,80,0")
        hx2 = self.add_host(dpid)
        self.centerless_ap.append(apx2)

        dpid, apx3 = self.add_ap(wlans=2, position="40,60,0")
        hx3 = self.add_host(dpid)
        self.centerless_ap.append(apx3)

        dpid, apx4 = self.add_ap(wlans=2, position="20,70,0")
        hx4 = self.add_host(dpid)
        self.centerless_ap.append(apx4)

        ap_count = 1
        for i in range(1, self.center_number+1):
            center_node = self.add_center_node(ap_count, i)
            ap_count = ap_count + 1
            normal_nodes = self.add_normal_nodes(ap_count, center_node, self.fanout)
            ap_count = ap_count + self.fanout

            self.center_nodes.append(center_node)
            self.normal_nodes_dist.setdefault(center_node['ap'].name, normal_nodes)
        
        
        info("Configure nodes...\n")
        self.net.configureNodes()

        info("Add Links...\n")
        self.add_center_links()
        self.add_normal_links()

        #### Centerless Part
        self.net.addLink(hx1, apx1)
        self.net.addLink(hx2, apx2)
        self.net.addLink(hx3, apx3)
        self.net.addLink(hx4, apx4)

        self.net.addLink(apx1, intf=f"{apx1.name}-wlan2", cls=mesh, ssid="mesh-ap5", channel=8)
        self.net.addLink(apx2, intf=f"{apx2.name}-wlan2", cls=mesh, ssid="mesh-ap5", channel=8)
        self.net.addLink(apx3, intf=f"{apx3.name}-wlan2", cls=mesh, ssid="mesh-ap5", channel=8)
        self.net.addLink(apx4, intf=f"{apx4.name}-wlan2", cls=mesh, ssid="mesh-ap5", channel=8)
        self.port_to_mesh[f"{apx1.name}-mp2"] = "mesh-ap5"
        self.port_to_mesh[f"{apx2.name}-mp2"] = "mesh-ap5"
        self.port_to_mesh[f"{apx3.name}-mp2"] = "mesh-ap5"
        self.port_to_mesh[f"{apx4.name}-mp2"] = "mesh-ap5"


    def start_aps(self):
        self.start_center()
        self.start_normal()
        self.start_centerless()

