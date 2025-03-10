from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json

class FlowData(BaseModel):
    datapath_id: str
    priority: int
    match: str
    instructions: str
    buffer_id: int | None = None
    command: str | None = None
    idle_timeout: int | None = None
    hard_timeout: int | None = None
    cookie: int | None = None
    flags: int | None = None

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化模板引擎
templates = Jinja2Templates(directory="templates")

# 示例数据
flow_items = []

@app.get("/api/flow-items")
async def get_flow_items():
    return flow_items

@app.post("/process_flow")
async def process_flow(flow_data: FlowData):
    flow_items.append(flow_data)
    return {"message": "Flow data received and processed."}

# 返回包含流表项的 HTML 页面
@app.get("/flow-table", response_class=HTMLResponse)
async def flow_table(request: Request):
    # 将 Python 数据转换为合法的 JSON 字符串
    flow_items_json = json.dumps([item.model_dump() for item in flow_items])

    # 渲染 HTML 模板并返回
    return templates.TemplateResponse(
        "flow_table.html",
        {"request": request, "flow_items_json": flow_items_json}
    )

# 启动 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
