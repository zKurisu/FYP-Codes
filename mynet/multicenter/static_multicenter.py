from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import mesh, wmediumd
from mn_wifi.wmediumdConnector import interference

from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from math import pi,cos,sin
from utils.next_mac import next_mac

def add_center_node(ap_count, center_index, net):
    posi_x = center_index * 30
    posi_y = 40
    position = f"{posi_x},{posi_y},0"
    name = f"ap{ap_count}"
    # hex_index = hex(index)
    host_mac = next_mac("host", ap_count)
    ap_mac = next_mac("ap", ap_count)

    info(f"Add center ap: {ap_mac}\n")
    ap = net.addAccessPoint(name, wlans=3, position=position, mac=ap_mac)
    # host = net.addHost(f"h{index}", mac=f"00:00:00:00:{hex_index}:00")
    info(f"Add center host: {host_mac}\n")
    host = net.addHost(f"h{ap_count}", mac=host_mac)

    return {
            # "ap": ap, "host": host, "hex_index": hex_index,
            "ap": ap, "host": host, 
            "position": {"x": posi_x, "y": posi_y}
            }

# Position depends on center_position
# Fanout depends on number specified
# def add_normal_nodes(center, number, net):
def add_normal_nodes(ap_count, center, number, net):
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
        ap = net.addAccessPoint(name, wlans=2, position=position, mac=ap_mac)
        # host = net.addHost(f"normal{i}-host", mac=f"00:00:00:00:{center_hex}:{normal_hex}")
        info(f"Add normal host: {host_mac}\n")
        host = net.addHost(f"h{i}", mac=host_mac)
        normal_nodes.append({"ap": ap, "host": host, "position": position})
    return normal_nodes

# Center and host
# Center Mesh, name: mesh-center
def add_center_links(center_nodes, net):
    for node in center_nodes:
        intf = f"{node["ap"].name}-wlan2"
        info(f"Add center link: {intf}\n")
        net.addLink(node["host"], node["ap"])
        net.addLink(node["ap"], intf=intf, cls=mesh, ssid="mesh-center", channel=5)

# Normal and host
# Local mesh, name: mesh-apx
def add_normal_links(center_nodes, normal_nodes_dist, net):
    for center_node in center_nodes:
        center_ap_name = center_node["ap"].name
        center_intf = f"{center_ap_name}-wlan3"
        ssid = f"mesh-{center_ap_name}"
        info(f"Add normal link: {center_intf}\n")
        net.addLink(center_node["ap"], intf=center_intf, cls=mesh, ssid=ssid, channel=8)

        for normal_node in normal_nodes_dist[center_ap_name]:
            normal_ap_name = normal_node["ap"].name
            normal_intf = f"{normal_ap_name}-wlan2"
            info(f"Add normal link: {normal_intf}\n")
            net.addLink(normal_node["host"], normal_node["ap"])
            net.addLink(normal_node["ap"], intf=normal_intf, cls=mesh, ssid=ssid, channel=8)

def start_center(center_nodes, c):
    for node in center_nodes:
        node["ap"].start(c)

def start_normal(normal_nodes_dist, c):
    for nodes in list(normal_nodes_dist.values()):
        for node in nodes:
            node["ap"].start(c)

def MultiCenterTopo():
    info("Create net...\n")
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("Create nodes...\n")
    center_nodes = []
    normal_nodes_dist = {} # Key is center_node
    center_number = 2 ################### Specific Part
    fanout = 1 ################### Specific Part
    ap_count = 1
    for i in range(1, center_number+1):
        center_node = add_center_node(ap_count, i, net)
        ap_count = ap_count + 1
        normal_nodes = add_normal_nodes(ap_count, center_node, fanout, net)
        ap_count = ap_count + fanout

        center_nodes.append(center_node)
        normal_nodes_dist.setdefault(center_node['ap'].name, normal_nodes)
    # c0 = net.addController("c0")
    c0 = net.addController("c0", controller=RemoteController, ip='127.0.0.1', port=6654)
    info(c0)
    
    info("Set propagation model...\n")
    net.setPropagationModel(model="logDistance", exp=5)
    info("Set plotGraph...\n")
    net.plotGraph(max_x=150, max_y=100)

    info("Configure nodes...\n")
    net.configureNodes()

    info("Add Links...\n")
    add_center_links(center_nodes, net)
    add_normal_links(center_nodes, normal_nodes_dist, net)

    info("Build net...\n")
    net.build()
    c0.start()
    start_center(center_nodes, [c0])
    start_normal(normal_nodes_dist, [c0])

    info("CLI Start...\n")
    CLI(net)

    info("Net stop...\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    MultiCenterTopo()
