# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ether
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.topology.api import get_switch
from ryu.topology import event
from ryu.app.wsgi import WSGIApplication, ControllerBase, route
from ryu.lib import hub

import httpx
import re
import networkx as nx
import threading
import json
from webob import Response
from operator import attrgetter
from mygrpc.python.apcontrol.apcontrol_client import run as rpcClientRun
from mygrpc.python.apcontrol.apcontrol_client import getAPLinks as rpcGetAPLinks

def add_CROS_header(method):
    def wrapper(*args, **kwargs):
        response = method(*args, **kwargs)
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    return wrapper

class RestAPIController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(RestAPIController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data['simple_switch_app']
    
    @route("Topology", "/topology", methods=['GET'])
    @add_CROS_header
    def _get_topo(self, req):
        json_data = json.dumps({
            "nodes": list(self.simple_switch_app.net.nodes),
            "edges": list(self.simple_switch_app.net.edges),
            "type": "graph"
        }).encode('utf-8')
        response = Response(content_type="application/json", body=json_data)
        return response
    
    @route("Flow table history", "/flowTable/history", methods=['GET'])
    @add_CROS_header
    def _get_flow_table_history(self, req):
        json_data = json.dumps({
            "total_entities": self.simple_switch_app.switch_flow_history,
            "type": "flowTableHistory"
        }).encode('utf-8')
        return Response(content_type="application/json", body=json_data)
    
    @route("Flow table current", "/flowTable/current", methods=['GET'])
    @add_CROS_header
    def _get_flow_table_current(self, req):
        json_data = json.dumps({
            "total_entities": self.simple_switch_app.switch_flow_entities,
            "type": "flowTableCurrent"
        }).encode('utf-8')
        return Response(content_type="application/json", body=json_data)
    
    @route("Mac to port table", "/macToPortTable", methods=['GET'])
    @add_CROS_header
    def _get_mac_to_port(self, req):
        json_data = json.dumps({
            "total_mac_to_port": self.simple_switch_app.mac_to_port,
            "type": "macToPortTable"
        }).encode('utf-8')
        return Response(content_type="application/json", body=json_data)
    
    @route("Port info", "/portInfo", methods=['GET'])
    @add_CROS_header
    def _get_port_info(self, req):
        json_data = json.dumps({
            "total_port_infos": self.simple_switch_app.switch_port_info,
            "type": "portInfo"
        }).encode('utf-8')
        return Response(content_type="application/json", body=json_data)
    
    @route("statistics", "/statistics", methods=['GET'])
    @add_CROS_header
    def _get_statistics(self, req):
        json_data = json.dumps({
            "total_statistics": self.simple_switch_app.switch_statistics,
            "type": "statistics"
        }).encode('utf-8')
        return Response(content_type="application/json", body=json_data)
    
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switch_host = {}
        self.switch_map = {}
        self.switch_statistics = {}
        self.switch_flow_entities = {}
        self.switch_flow_history = {}
        self.switch_port_info = {}
        self.count = 0
        self.topology_api_app = self
        self.net = nx.Graph()
        self.arp_table = {
                    '10.0.0.1':'00:00:00:00:00:01',
                    '10.0.0.2':'00:00:00:00:00:02',
                    '10.0.0.3':'00:00:00:00:00:03',
                    '10.0.0.4':'00:00:00:00:00:04',
                    '10.0.0.5':'00:00:00:00:00:05',
                    '10.0.0.6':'00:00:00:00:00:06',
                    '10.0.0.7':'00:00:00:00:00:07',
                    '10.0.0.8':'00:00:00:00:00:08',
                    '10.0.0.9':'00:00:00:00:00:09',
                    '10.0.0.10':'00:00:00:00:00:0a',
                    '10.0.0.11':'00:00:00:00:00:0b',
                    '10.0.0.12':'00:00:00:00:00:0c',
                    '10.0.0.13':'00:00:00:00:00:0d',
                    '10.0.0.14':'00:00:00:00:00:0e',
                    '10.0.0.15':'00:00:00:00:00:0f',
                    '10.0.0.16':'00:00:00:00:00:10',
                    '10.0.0.17':'00:00:00:00:00:11',
                    '10.0.0.18':'00:00:00:00:00:12',
                    '10.0.0.19':'00:00:00:00:00:13',
                    '10.0.0.20':'00:00:00:00:00:14',
                    }
        threading.Timer(5, function=self.update_links).start()
        self.monitor_thread = hub.spawn(self._monitor)


        wsgi = kwargs['wsgi']
        wsgi.register(RestAPIController, { "simple_switch_app": self })

    def _monitor(self):
        while True:
            for dp in self.switch_map.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # 检测 table-miss 是否存在
        table_miss_exists = False
        for stat in body:
            if stat.priority == 0 and not stat.match:  # 无匹配条件且优先级为0
                table_miss_exists = True
                break

        # 如果缺失，则重新添加
        if not table_miss_exists:
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                            ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 0, match, actions)
            print("Add Default flow entities\n")
        
        flow_entities = []
        for stat in sorted([flow for flow in body if flow.priority == 1],
                        key=lambda flow: (
                            flow.match.get('in_port', 0),  # 使用get方法提供默认值
                            flow.match.get('eth_dst', '00:00:00:00:00:00')
                        )):
            # 获取输出端口，处理可能的缺失情况
            out_port = 0
            if stat.instructions and stat.instructions[0].actions:
                out_port = stat.instructions[0].actions[0].port
            # 格式化字符串并添加到列表
            flow_entity =  {
                    "in_port": stat.match.get('in_port', 0),
                    "eth_dst": stat.match.get('eth_dst', '00:00:00:00:00:00'),
                    "out_port": out_port,
                    "packet_count": stat.packet_count,
                    "byte_count": stat.byte_count
            }
            flow_entities.append(flow_entity)    
        self.switch_flow_entities[ev.msg.datapath.id] = flow_entities
    
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        statistics = []
        for stat in sorted(body, key=attrgetter('port_no')):
            statistics.append({
                "port_no": stat.port_no,
                "rx_packets": stat.rx_packets,
                "rx_bytes": stat.rx_bytes,
                "rx_errors": stat.rx_errors,
                "tx_packets": stat.tx_packets,
                "tx_bytes": stat.tx_bytes,
                "tx_errors": stat.tx_errors,
            })
        
        self.switch_statistics[ev.msg.datapath.id] = statistics

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        dpid = format(datapath.id, "d").zfill(16)
        self.switch_map[dpid] = datapath
        req = parser.OFPPortDescStatsRequest(datapath, 0)
        datapath.send_msg(req)

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print("Add Default flow entities\n")


    def add_flow(self, datapath, priority, match, actions, buffer_id=None, idle_timeout=65535):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match, idle_timeout=idle_timeout,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority, idle_timeout=idle_timeout,
                                    match=match, instructions=inst)
        
        hex_dpid = format(datapath.id, "x")
        self.print_flow_mod(mod, hex_dpid)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def _port_desc_stats_reply_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = format(datapath.id, "d").zfill(16)
        hex_dpid = format(datapath.id, "x")
        self.switch_port_info.setdefault(hex_dpid, 0)
        
        self.switch_port_info[hex_dpid] = []
        for p in ev.msg.body:
            port_name = p.name.decode('utf-8')
            self.switch_port_info[hex_dpid].append({
                "port_no": p.port_no,
                "port_name": port_name,
                "mac": p.hw_addr
            })
            if re.search(r"eth" , port_name):
                host_mac = "00:00:00:00:00:" + hex_dpid[len(hex_dpid)-2:]
                print(f"Host mac is {host_mac}")
                self.switch_host[dpid] = host_mac
                self.net.add_node(host_mac) # Add host to net
                self.net.add_edge(host_mac, dpid, port_no=p.port_no) # Add edge for AP and Host

                self.logger.info("Port No: %d, Name: %s, HW Addr: %s",
                                p.port_no, p.name, p.hw_addr)
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        out_port = None

        pkt_arp = pkt.get_protocol(arp.arp)
        if eth.ethertype == 2054:
            print("arp")
            self.handle_arp(datapath, in_port, eth, pkt_arp)
            return

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        # self.logger.info("PacketIn: src=%s, dst=%s, ethertype=0x%04x", eth.src, eth.dst, eth.ethertype)

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        # print_mac_to_port(self.mac_to_port)
        # self.logger.info(self.mac_to_port)
        print(f"src: {src}, dst: {dst}")
        if self.net.has_node(dst) and self.net.has_node(src):
            print("%s in self.net" % dst)
            # print(self.net.edges(data=True))

            try:
                path = nx.shortest_path(self.net, src, dst)
                next_match = parser.OFPMatch(eth_dst=dst)
                back_match = parser.OFPMatch(eth_dst=src)
                print(f"Path is: {path}")

                for on_path_switch in range(1, len(path)-1):
                    now_switch = path[on_path_switch]
                    next_switch = path[on_path_switch+1]
                    back_switch = path[on_path_switch-1]
                    print(self.net[now_switch][next_switch])
                    print(self.net[now_switch][back_switch])
                    next_port = self.net[now_switch][next_switch]['port_no']
                    back_port = self.net[now_switch][back_switch]['port_no']
                    actions = [parser.OFPActionOutput(next_port)]
                    self.add_flow(datapath=self.switch_map[now_switch], match=next_match, actions=actions, priority=1, idle_timeout=10)
                    
                    actions = [parser.OFPActionOutput(back_port)]
                    self.add_flow(datapath=self.switch_map[now_switch], match=back_match, actions=actions, priority=1, idle_timeout=10)
                    print("now switch:%s" % now_switch)
            except nx.NetworkXNoPath:
                print(f"No path between {src} and {dst}")
        else:
            out_port = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(out_port)]

            data = None
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                data = msg.data

            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                    in_port=in_port, actions=actions, data=data)
            datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def _switch_enter_handler(self, ev):
        print("............Switch Enter")
        switch_list = get_switch(self.topology_api_app, None)
        switches = [format(switch.dp.id, "d").zfill(16) for switch in switch_list]
        response = rpcGetAPLinks()
        links = response.ap_links
        # print(f"RPC Return Links: {links}")

        for switch in switches:
            if self.net.has_node(switch):
                continue
            else:
                self.net.add_node(switch)
        
        for link in links:
            if self.net.has_edge(link.src_dpid, link.dst_dpid):
                continue
            else:
                self.net.add_edge(link.src_dpid, link.dst_dpid, port_no=link.port_no)
        # print(f"Nodes: {self.net.nodes}")
        # print(f"Edges: {self.net.edges(data=True)}")
    
    @set_ev_cls(event.EventSwitchLeave)
    def _switch_leave_handler(self, ev):
        print("............Switch Leave")
        switch = format(ev.switch.dp.id, "d").zfill(16)

        if self.net.has_node(switch):
            self.net.remove_node(switch)
            self.net.remove_node(self.switch_host[switch])
        
        # print(f"Left Nodes: {self.net.nodes}")
        # print(f"Left Edges: {self.net.edges}")

#     @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
#     def _add_link_and_node(self, ev):
#         print(".........Link Add handler")
#         link = ev.link
#         src_node = link.src
#         dst_node = link.dst
# 
#         if self.net.has_edge(src_node, dst_node):
#             return
# 
#         self.net.add_edge(src_node, dst_node)
#         print(f".........Link Added: ({src_node}, {dst_node})")
# 
#     @set_ev_cls(event.EventLinkDelete, MAIN_DISPATCHER)
#     def _del_link_and_node(self, ev):
#         print(".........Link Delete handler")
#         link = ev.link
#         src_node = link.src
#         dst_node = link.dst
# 
#         if self.net.has_edge(src_node, dst_node):
#             self.net.remove_edge(src_node, dst_node)
#             print(f".........Link Deleted: ({src_node}, {dst_node})")
#         else:
#             return

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        parser = datapath.ofproto_parser
        portInfo = msg.desc
        target_dpid = format(datapath.id, "d").zfill(16)

        self.logger.info(f"Detected {portInfo.name} status change.")
        if msg.reason == ofp.OFPPR_ADD:
            self.logger.info(f"{portInfo.name} is new added.")
        elif msg.reason == ofp.OFPPR_DELETE:
            self.logger.info(f"{portInfo.name} is deleted.")
        elif msg.reason == ofp.OFPPR_MODIFY:
            self.logger.info(f"{portInfo.name} is modified.")
            if portInfo.config == ofp.OFPPC_PORT_DOWN:
                port_attr = nx.get_edge_attributes(self.net, "port")

                for edge, port in port_attr.items():
                    if port == portInfo.port_no and datapath.id in edge:
                        self.net.remove_edge(*edge)

                self.logger.info(f"{portInfo.name} is down by administrator.")
                target_host = self.switch_host[target_dpid]

                if target_host:
                    print("Delete flow????")
                    # for switch in self.switch_map.values():
                    #     match = parser.OFPMatch(eth_dst=target_host)
                    #     self._delete_flows(switch, match)

                    #     match = parser.OFPMatch(eth_src=target_host)
                    #     self._delete_flows(switch, match)
            else:
                dpid = format(datapath.id, "x")
                self.logger.info(f"{portInfo.name} is up.")
                self.logger.info(f"Call RPC to Mininet for mesh connection.")
                self.logger.info(f"{dpid}: {portInfo.name}")
                status = rpcClientRun(f"{dpid}", portInfo.name)
                self.logger.info(f"Mininet response: {status}")
        
    
    def _delete_flows(self, datapath, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        hex_dpid = format(datapath.id, "x")

        # 构建 OFPFlowMod 消息，删除匹配的流表项
        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            command=ofproto.OFPFC_DELETE,
            match=match,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            table_id=ofproto.OFPTT_ALL,
        )

        # 发送消息
        self.print_flow_mod(flow_mod, hex_dpid)
        datapath.send_msg(flow_mod)
        print(f"Deleted flows with match: {match}")
	
    def send_packet(self, dp, port, pkt):
        ofproto = dp.ofproto
        parser = dp.ofproto_parser
        pkt.serialize()
        data = pkt.data
        action = [parser.OFPActionOutput(port=port)]

        out = parser.OFPPacketOut(
                datapath=dp, buffer_id = ofproto.OFP_NO_BUFFER,
                in_port = ofproto.OFPP_CONTROLLER,
                actions=action, data=data)

        dp.send_msg(out)

    
    def handle_arp(self, dp, port, pkt_ethernet, pkt_arp):
        if pkt_arp.opcode != arp.ARP_REQUEST:
            return
        
        if self.arp_table.get(pkt_arp.dst_ip) == None:
            return
        get_mac = self.arp_table[pkt_arp.dst_ip]
        

        pkt = packet.Packet()
        pkt.add_protocol(
            ethernet.ethernet(
                ethertype=ether.ETH_TYPE_ARP,
                dst = pkt_ethernet.src,
                src = get_mac
            )
        )

        pkt.add_protocol(
            arp.arp(
                opcode=arp.ARP_REPLY,
                src_mac= get_mac,
                src_ip = pkt_arp.dst_ip,
                dst_mac= pkt_arp.src_mac,
                dst_ip = pkt_arp.src_ip 
            )
        )

        self.send_packet(dp, port, pkt)

    def update_links(self):
        edges_to_remove = [
            (src, dst) for src, dst in self.net.edges
            if (not str(src).startswith("00")) and (not str(dst).startswith("00"))
        ]
        self.net.remove_edges_from(edges_to_remove)
        response = rpcGetAPLinks()
        if response != None:
            links = response.ap_links
            # print(f"Links from Mininet: {links}")
            for link in links:
                self.net.add_edge(link.src_dpid, link.dst_dpid, port_no=link.port_no)

        threading.Timer(5, function=self.update_links).start()
        print("Timer run...")

    def print_flow_mod(self, mod, dpid):
        ofproto = mod.datapath.ofproto
        parser = mod.datapath.ofproto_parser

        # 构建要发送的数据
        # print(f"print_flow_mode: {dpid}\n")
        flow_data = {
            "datapath_id": dpid,
            "priority": mod.priority,
            "match": str(mod.match),
            "instructions": str(mod.instructions),
            "buffer_id": mod.buffer_id if mod.buffer_id != ofproto.OFP_NO_BUFFER else None,
            "command": None,
            "idle_timeout": mod.idle_timeout if mod.idle_timeout != 0 else None,
            "hard_timeout": mod.hard_timeout if mod.hard_timeout != 0 else None,
            "cookie": mod.cookie if mod.cookie != 0 else None,
            "flags": mod.flags if mod.flags != 0 else None,
        }

        # 设置 command 字段
        if mod.command == ofproto.OFPFC_ADD:
            flow_data["command"] = "ADD"
        elif mod.command == ofproto.OFPFC_MODIFY:
            flow_data["command"] = "MODIFY"
        elif mod.command == ofproto.OFPFC_DELETE:
            flow_data["command"] = "DELETE"
        else:
            flow_data["command"] = str(mod.command)

        self.switch_flow_history.setdefault(dpid, [])
        self.switch_flow_history[dpid].append(flow_data)

def print_mac_to_port(mac_to_port):
    # 发送 POST 请求
    fastapi_url = "http://127.0.0.1:8000/process_mac_to_port"  # FastAPI 程序的 URL
    try:
        with httpx.Client() as client:
            response = client.post(fastapi_url, json=mac_to_port)
            if response.status_code == 200:
                pass
                # print("Mac to port table successfully sent to FastAPI.")
            else:
                print(f"Failed to send mac to port table. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending POST request: {e}")

