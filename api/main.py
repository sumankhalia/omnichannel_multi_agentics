from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database.db_engine import engine, SessionLocal
from database.models import Base, Customer
from utils.data_generator import generate_data

from core.agents.insight_agent import ask_with_data
from core.agents.war_room_agent import run_war_room

# ---------------------------------------------------
# APP
# ---------------------------------------------------

app = FastAPI(title="Omnichannel Multi-Agentics API")

# ---------------------------------------------------
# CORS (React / Frontend / Render Safe)
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------
# STARTUP INITIALIZATION
# ---------------------------------------------------

@app.on_event("startup")
def initialize_database():

    db = SessionLocal()

    try:
        customer_count = db.query(Customer).count()

        if customer_count == 0:
            print("EMPTY DATABASE → GENERATING DATA...")
            generate_data()
            print("SAMPLE DATA GENERATED")
        else:
            print(f"DATABASE READY → {customer_count} customers")

    except Exception as e:
        print("DATABASE INITIALIZATION ERROR:", str(e))

    finally:
        db.close()

# ---------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------

class QueryRequest(BaseModel):
    query: str
    market_context: str | None = None

# ---------------------------------------------------
# AGENT LAB (Fast Tactical Agent)
# ---------------------------------------------------

@app.post("/agent/lab")
def agent_lab(req: QueryRequest):

    response = ask_with_data(req.query)

    return response

# ---------------------------------------------------
# WAR ROOM (Multi-Agent Strategic Engine)
# ---------------------------------------------------

@app.post("/agent/warroom")
def agent_warroom(req: QueryRequest):

    response = run_war_room(req.query, req.market_context)

    return response

# ---------------------------------------------------
# HEALTH CHECK (CRITICAL FOR RENDER)
# ---------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "API running"}
