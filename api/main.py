from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.agents.insight_agent import ask_with_data
from core.agents.war_room_agent import run_war_room
from api.routes.analytics_routes import router as analytics_router

# Optional (only if using SQLAlchemy DB)
from database.db_engine import engine
from database.models import Base

# Optional (only if using seed logic)
from utils.data_generator import generate_data


# =====================================================
# APPLICATION INITIALIZATION
# =====================================================

app = FastAPI(
    title="Omnichannel Intelligence Engine",
    description="Analytics + AI Agents + War Room Intelligence",
    version="1.0"
)

# =====================================================
# CORS CONFIGURATION (FOR REACT / FRONTENDS)
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Dev mode → restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DATABASE INITIALIZATION (SAFE + PROFESSIONAL)
# =====================================================

@app.on_event("startup")
def startup_event():

    print("System Booting...")

    try:
        Base.metadata.create_all(bind=engine)
        print("Database schema verified")

        generate_data()
        print("Demo data ready")

    except Exception as e:
        print("Startup Error:", str(e))


# =====================================================
# ROUTERS (ANALYTICS ENGINE)
# =====================================================

app.include_router(analytics_router)


# =====================================================
# REQUEST MODELS
# =====================================================

class QueryRequest(BaseModel):
    query: str
    market_context: str | None = None


# =====================================================
# HEALTH CHECKS (CRITICAL FOR RENDER)
# =====================================================

@app.get("/")
def root():
    return {"status": "ENGINE_RUNNING"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# =====================================================
# SINGLE AGENT ENDPOINT
# =====================================================

@app.post("/agent/lab")
def agent_lab(req: QueryRequest):

    print("Tactical Agent Activated")

    return ask_with_data(req.query)


# =====================================================
# WAR ROOM MULTI-AGENT ENDPOINT
# =====================================================

@app.post("/agent/warroom")
def agent_warroom(req: QueryRequest):

    print("War Room Activated")

    return run_war_room(req.query, req.market_context)