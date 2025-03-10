from mcds.gen_UDG import generate_connected_udg
from socket_util import socket_server

from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import OVSAP
from mininet.cli import CLI

def add_aps(n=10, signal_range=31.484254489723796, seed=20):
    nodes_dict, _ = generate_connected_udg(
        n=n,
        signal_range=signal_range,
        seed=seed
    )

    dpid_nodes_dict = {}
    for k in nodes_dict.keys():
        dpid = 10**15 + k
        dpid_nodes_dict[dpid] = nodes_dict[k]

    data = {
            "positions": dpid_nodes_dict,
            "signal_range": signal_range
    }
    center_dpids = socket_server.listen_connect(data)

def MultiCenter():
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    c0 = net.addController("c0")

    net.setPropagationModel(model="logDistance", exp=5)
    net.configureNodes()

    net.build()
    c0.start()

    CLI(net)
    net.stop()

MultiCenter()
