from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.chat_routes import router
from database.db_engine import engine, SessionLocal
from database.models import Base, Customer
from utils.data_generator import generate_data

app = FastAPI()

# CORS FIX (THIS is your issue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev. Later restrict.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ALWAYS CREATE TABLES
Base.metadata.create_all(bind=engine)


def initialize_database():
    db = SessionLocal()

    try:
        customer_count = db.query(Customer).count()

        if customer_count == 0:
            print("EMPTY DATABASE → GENERATING DATA")
            generate_data()
        else:
            print(f"✅ DATABASE READY → {customer_count} customers")

    finally:
        db.close()


initialize_database()

app.include_router(router)
