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
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

import httpx
import re
from mygrpc.python.apcontrol.apcontrol_client import run as rpcClientRun


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.switch_hosts = {}
        self.switches = []
        self.count = 0

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        self.switches.append(datapath)
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


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        
        hex_dpid = format(datapath.id, "x")
        print_flow_mod(mod, hex_dpid)
        datapath.send_msg(mod)
    
    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = format(datapath.id, "d").zfill(16)
        self.switch_hosts.setdefault(dpid, {})
        
        for p in ev.msg.body:
            port_name = p.name.decode('utf-8')
            if re.search(r"eth" , port_name):
                self.switch_hosts[dpid].setdefault(p.port_no, "")
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
        print_mac_to_port(self.mac_to_port)
        # self.logger.info(self.mac_to_port)

        if in_port in self.switch_hosts[dpid].keys():
            self.switch_hosts[dpid][in_port] = src
            self.logger.info(f"{dpid} connect host: {src} on port {in_port}")

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
    
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
                self.logger.info(f"{portInfo.name} is down by administrator.")
                target_hosts = self.switch_hosts[target_dpid].values()

                if len(target_hosts) > 0:
                    for hw_addr in target_hosts:
                        for switch in self.switches:
                            match = parser.OFPMatch(eth_dst=hw_addr)
                            self._delete_flows(switch, match)

                            match = parser.OFPMatch(eth_src=hw_addr)
                            self._delete_flows(switch, match)

                    self.mac_to_port = {}
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
        print_flow_mod(flow_mod, hex_dpid)
        datapath.send_msg(flow_mod)
        self.logger.info(f"Deleted flows with match: {match}")


def print_flow_mod(mod, dpid):
    ofproto = mod.datapath.ofproto
    parser = mod.datapath.ofproto_parser

    # 构建要发送的数据
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

    # 发送 POST 请求
    fastapi_url = "http://127.0.0.1:8000/process_flow"  # FastAPI 程序的 URL
    try:
        with httpx.Client() as client:
            response = client.post(fastapi_url, json=flow_data)
            if response.status_code == 200:
                pass
                # print("Flow data successfully sent to FastAPI.")
            else:
                print(f"Failed to send flow data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending POST request: {e}")

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
