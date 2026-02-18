from fastapi import FastAPI

from api.routes.chat_routes import router

from database.db_engine import engine, SessionLocal
from database.models import Base, Customer

from utils.data_generator import generate_data


app = FastAPI()


# -----------------------------
# ROOT / HEALTH ENDPOINT
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "healthy",
        "service": "Omnichannel Multi-Agentics API"
    }


# -----------------------------
# DATABASE SETUP
# -----------------------------
Base.metadata.create_all(bind=engine)


def initialize_database():

    db = SessionLocal()

    try:
        customer_count = db.query(Customer).count()

        if customer_count == 0:
            print("EMPTY DATABASE DETECTED → GENERATING SAMPLE DATA")
            generate_data()
        else:
            print(f"DATABASE READY → {customer_count} customers loaded")

    finally:
        db.close()


# RUN ON STARTUP
initialize_database()


# -----------------------------
# ROUTES
# -----------------------------
app.include_router(router)
