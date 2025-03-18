from mynet.mynet import MyNetBase, set_mode

from mn_wifi.link import mesh
from mininet.log import info
from math import pi,cos,sin
from utils.next_mac import next_mac

class MyNet(MyNetBase):
    def __init__(self):
        super(MyNet, self).__init__()
        self.aps = []
        self.hosts = []
        self.center_nodes = []
        self.normal_nodes_dist = {}
        self.center_number = 2 ################### Specific Part
        self.fanout = 1 ################### Specific Part
        pass

    def add_center_node(self, ap_count, center_index):
        posi_x = center_index * 30
        posi_y = 40
        position = f"{posi_x},{posi_y},0"
        name = f"ap{ap_count}"
        # hex_index = hex(index)
        host_mac = next_mac("host", ap_count)
        ap_mac = next_mac("ap", ap_count)

        info(f"Add center ap: {ap_mac}\n")
        ap = self.net.addAccessPoint(name, wlans=3, position=position, mac=ap_mac)
        self.aps.append(ap)
        # host = net.addHost(f"h{index}", mac=f"00:00:00:00:{hex_index}:00")
        info(f"Add center host: {host_mac}\n")
        host = self.net.addHost(f"h{ap_count}", mac=host_mac)
        self.hosts.append(host)

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
            name = f"ap{i}"
            degree = degree_init + degree_gap * (i-1)
            # center_hex = center["hex_index"]
            # normal_hex = hex(i)
            host_mac = next_mac("host", i)
            ap_mac = next_mac("ap", i)

            posi_x = distance * cos(degree) + center_x
            posi_y = distance * sin(degree) + center_y
            
            # info(f"Position for {name} is {posi_x},{posi_y},0 \n")
            position = f"{posi_x},{posi_y},0"

            info(f"Add normal ap: {ap_mac}\n")
            ap = self.net.addAccessPoint(name, wlans=2, position=position, mac=ap_mac)
            self.aps.append(ap)
            # host = net.addHost(f"normal{i}-host", mac=f"00:00:00:00:{center_hex}:{normal_hex}")
            info(f"Add normal host: {host_mac}\n")
            host = self.net.addHost(f"h{i}", mac=host_mac)
            self.aps.append(host)
            normal_nodes.append({"ap": ap, "host": host, "position": position})
        return normal_nodes

    # Center and host
    # Center Mesh, name: mesh-center
    def add_center_links(self):
        for node in self.center_nodes:
            intf = f"{node["ap"].name}-wlan2"
            info(f"Add center link: {intf}\n")
            self.net.addLink(node["host"], node["ap"])
            self.net.addLink(node["ap"], intf=intf, cls=mesh, ssid="mesh-center", channel=5)

    # Normal and host
    # Local mesh, name: mesh-apx
    def add_normal_links(self):
        for center_node in self.center_nodes:
            center_ap_name = center_node["ap"].name
            center_intf = f"{center_ap_name}-wlan3"
            ssid = f"mesh-{center_ap_name}"
            info(f"Add normal link: {center_intf}\n")
            self.net.addLink(center_node["ap"], intf=center_intf, cls=mesh, ssid=ssid, channel=8)

            for normal_node in self.normal_nodes_dist[center_ap_name]:
                normal_ap_name = normal_node["ap"].name
                normal_intf = f"{normal_ap_name}-wlan2"
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

    def get_ap_list(self):
        return self.aps

    def get_host_list(self):
        return self.hosts

    @set_mode
    def config(self):
        info("Create nodes...\n")
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


    def start_aps(self):
        self.start_center()
        self.start_normal()
