from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.agents.insight_agent import ask_with_data
from core.agents.war_room_agent import run_war_room

app = FastAPI()

# ✅ CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev mode (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    market_context: str | None = None


@app.post("/agent/lab")
def agent_lab(req: QueryRequest):
    return ask_with_data(req.query)


@app.post("/agent/warroom")
def agent_warroom(req: QueryRequest):
    return run_war_room(req.query, req.market_context)
