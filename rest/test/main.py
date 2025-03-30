from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ryu_wsgi": "http://127.0.0.1:8000"
        }
    )
    
######## TMP TEST
# "ryu_wsgi": "http://192.168.1.109:8080/"
# "ryu_wsgi": "http://127.0.0.1:8000"
# Node List: ["node1", "node2", "node3", "node4"]
# Edge List: [
# {"src": "node2", "dst": "node1"},
# {"src": "node3", "dst": "node1"},
# {"src": "node4", "dst": "node1"},
# ]
@app.get("/topology")
def get_topology():
    node_list = ["10000000000000001", "10000000000000002", "10000000000000003", "10000000000000004", "0000001", "0000002"]

    edge_list = [
        ("10000000000000002", "10000000000000001"),
        ("10000000000000003", "10000000000000001"),
        ("10000000000000004", "10000000000000001"),
        ("0000001", "10000000000000001"),
        ("0000002", "10000000000000002"),
    ]

    response_content = json.dumps({
        "nodes": node_list,
        "edges": edge_list,
        "type": "graph"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 一行一行字符串返回?
@app.get("/flowTable/current")
def get_current_flow_table():
    total_entities = {
        "10001": [
            {
                "in_port": 0,
                "eth_dst": "00:00:00:00:00:01",
                "out_port": 3,
                "packet_count": 100,
                "byte_count": 1000
            },
        ],
        "10002": [
            {
                "in_port": 0,
                "eth_dst": "00:00:00:00:00:01",
                "out_port": 3,
                "packet_count": 100,
                "byte_count": 1000
            },
        ],
    }
    
    response_content = json.dumps({
        "total_entities": total_entities,
        "type": "flowTableCurrent"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 一行一行字符串返回?
@app.get("/flowTable/history")
def get_hostory_flow_table():
    total_entities = {
        "10001": [
            {
                "priority": 1,
                "match": "match string",
                "instruction": "instruction string",
                "buffer_id": 0,
                "command": "ADD",
                "idel_timeout": 100,
                "hard_timeout": 300,
                "cookie": "cookie string",
                "flags": 1
            },
        ],
        "10002": [
            {
                "priority": 1,
                "match": "match string",
                "instruction": "instruction string",
                "buffer_id": 0,
                "command": "ADD",
                "idel_timeout": 100,
                "hard_timeout": 300,
                "cookie": "cookie string",
                "flags": 1
            },
        ],
    }

    response_content = json.dumps({
        "total_entities": total_entities,
        "type": "flowTableHistory"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 
@app.get("/statistics")
def get_statistics():
    total_statistics = {
        "10001": [
            {
                "port_no": 1,
                "rx_packets": 10,
                "rx_bytes": 11,
                "rx_errors": 12,
                "tx_packets": 13,
                "tx_bytes": 14,
                "tx_errors": 15,
            }
        ],
        "10002": [
            {
                "port_no": 1,
                "rx_packets": 10,
                "rx_bytes": 11,
                "rx_errors": 12,
                "tx_packets": 13,
                "tx_bytes": 14,
                "tx_errors": 15,
            }
        ],
    }
    response_content = json.dumps({
        "total_statistics": total_statistics,
        "type": "statistics"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 
@app.get("/portInfo")
def get_port_info():
    total_port_infos = {
        "10001": [
            {
                "port_no": 1,
                "port_name": "eth1",
                "mac": "00:00:00:00:00:01",
            }
        ],
        "10002": [
            {
                "port_no": 2,
                "port_name": "eth2",
                "mac": "00:00:00:00:00:02",
            }
        ],
    }

    response_content = json.dumps({
        "total_port_infos": total_port_infos,
        "type": "portInfo"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 
@app.get("/macToPortTable")
def get_mac_to_port_table():
    total_mac_to_port = {
        "10001": {
            "00:00:00:00:00:01": 1,
            "00:00:00:00:00:02": 2,
        },
        "10002": {
            "00:00:00:00:00:01": 1,
            "00:00:00:00:00:02": 2,
        }
    }

    response_content = json.dumps({
        "total_mac_to_port": total_mac_to_port,
        "type": "macToPortTable"
        })
    return Response(response_content)

######### TMP TEST
