# FastAPI For find center

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Tuple
from mcds.find_MCDS import find_mcds

app = FastAPI()

class TopoData(BaseModel):
    positions: Dict[str, Tuple[float, float]]
    signal_range: float

@app.post("/find_center")
async def process_positions(request: TopoData):
    positions = request.positions
    signal_range = request.signal_range

    mcds, adjs = find_mcds(positions, signal_range)

    return {"status": "Positions processed successfully", "center_dpids": mcds, "adjacency": adjs}
