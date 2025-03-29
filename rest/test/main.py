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
    
######### TMP TEST
# Node List: ["node1", "node2", "node3", "node4"]
# Edge List: [
# {"src": "node2", "dst": "node1"},
# {"src": "node3", "dst": "node1"},
# {"src": "node4", "dst": "node1"},
# ]
@app.get("/topology")
def get_topology():
    node_list = ["node1", "node2", "node3", "node4"]

    edge_list = [
        {"src": "node2", "dst": "node1"},
        {"src": "node3", "dst": "node1"},
        {"src": "node4", "dst": "node1"},
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
    total_entities = [
        {
            "dpid": "10001",
            "entities": [
                "flow entities 1",
                "flow entities 2",
                "flow entities 3",
                "flow entities 4",
            ],
        },
        {
            "dpid": "10001",
            "entities": [
                "flow entities 1",
                "flow entities 2",
                "flow entities 3",
                "flow entities 4",
            ],
        }
    ]

    response_content = json.dumps({
        "total_entities": total_entities,
        "type": "flowTable"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 一行一行字符串返回?
@app.get("/flowTable/history")
def get_hostory_flow_table():
    total_entities = [
        {
            "dpid": "10001",
            "entities": [
                "flow entities 1",
                "flow entities 2",
                "flow entities 3",
                "flow entities 4",
            ],
        },
        {
            "dpid": "10002",
            "entities": [
                "flow entities 1",
                "flow entities 2",
                "flow entities 3",
                "flow entities 4",
            ],
        }
    ]

    response_content = json.dumps({
        "total_entities": total_entities,
        "type": "flowTable"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 
@app.get("/statistics")
def get_statistics():
    total_statistics = [
        {
            "dpid": "10001",
            "statistics": [
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
        },
        {
            "dpid": "10002",
            "statistics": [
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
        },
    ]
    response_content = json.dumps({
        "total_statistics": total_statistics,
        "type": "statistics"
        })
    return Response(response_content)

#### EXAMPLE DATA
# 
@app.get("/portInfo")
def get_port_info():
    total_port_infos = [
        {
            "dpid": "10001",
            "port_info": [
                {
                    "port_no": 1,
                    "port_name": "eth1",
                    "mac": "00:00:00:00:00:01",
                }
            ],
        },
        {
            "dpid": "10002",
            "port_info": [
                {
                    "port_no": 2,
                    "port_name": "eth2",
                    "mac": "00:00:00:00:00:02",
                }
            ],
        },
    ]
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
        "type": "macToPortTable"
        })
    return Response(response_content)

######### TMP TEST
