from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Tuple
from utils.find_MCDS import find_mcds
import json

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="rest/static"), name="static")

# 初始化模板引擎
templates = Jinja2Templates(directory="rest/templates")

@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ryu_wsgi": "http://192.168.1.20:8080"
        }
    )

class TopoData(BaseModel):
    positions: Dict[str, Tuple[float, float]]
    signal_range: float

@app.post("/find_center")
async def process_positions(request: TopoData):
    positions = request.positions
    signal_range = request.signal_range

    mcds, adjs = find_mcds(positions, signal_range)

    return {"status": "Positions processed successfully", "center_dpids": mcds, "adjacency": adjs}


########## Could Delete
# 定义内层字典的类型
# InnerDict = Dict[str, int]
# 
# # 定义外层字典的类型
# OuterDict = Dict[str, InnerDict]
# 
# class FlowData(BaseModel):
#     datapath_id: str
#     priority: int
#     match: str
#     instructions: str
#     buffer_id: int | None = None
#     command: str | None = None
#     idle_timeout: int | None = None
#     hard_timeout: int | None = None
#     cookie: int | None = None
#     flags: int | None = None
# 
# # 示例数据
# flow_items = []
# 
# @app.get("/api/flow-items")
# async def get_flow_items():
#     return flow_items
# 
# @app.post("/process_flow")
# async def process_flow(flow_data: FlowData):
#     flow_items.append(flow_data)
#     return {"message": "Flow data received and processed."}
# 
# # 返回包含流表项的 HTML 页面
# @app.get("/flow-table", response_class=HTMLResponse)
# async def flow_table(request: Request):
#     # 将 Python 数据转换为合法的 JSON 字符串
#     flow_items_json = json.dumps([item.model_dump() for item in flow_items])
# 
#     # 渲染 HTML 模板并返回
#     return templates.TemplateResponse(
#         "flow_table.html",
#         {"request": request, "flow_items_json": flow_items_json}
#     )
# 
# 
# app.state.global_mac_to_port = None
# @app.get("/api/mac_to_port-items")
# async def get_mac_to_port_items():
#     return app.state.global_mac_to_port
# 
# @app.post("/process_mac_to_port")
# async def process_mac_to_port(mac_to_port: OuterDict = Body(...)):
#     app.state.global_mac_to_port = mac_to_port
#     return {"message": "mac to port table received and processed."}
# 
# @app.get("/mac_to_port-table", response_class=HTMLResponse)
# async def mac_to_port_table(request: Request):
#     mac_to_port_items_json = json.dumps(app.state.global_mac_to_port)
# 
#     # 渲染 HTML 模板并返回
#     return templates.TemplateResponse(
#         "mac_to_port_table.html",
#         {"request": request, "mac_to_port_items_json": mac_to_port_items_json}
#     )
# 
# class IntfsDict(BaseModel):
#     name: str
#     port: int
#     mac: str
# APInfo = Dict[str, List[IntfsDict]]
# 
# @app.post("/process_apInfo")
# def process_apInfo(apInfo: APInfo):
#     app.state.apInfo = apInfo
#     return {"msg": f"FastAPI receive APInfo with {len(apInfo.keys())} ap"}
# 
# @app.get("/apInfo-table", response_class=HTMLResponse)
# def show_apInfo(request: Request):
#     # 将 Pydantic 模型对象转换为字典
#     apInfo_dict = {k: [v.dict() for v in lst] for k, lst in app.state.apInfo.items()}
#     apInfo_json = json.dumps(apInfo_dict)
#     return templates.TemplateResponse(
#         "apInfo_table.html",
#         {"request": request, "apInfo_json": apInfo_json}
#     )
# 
