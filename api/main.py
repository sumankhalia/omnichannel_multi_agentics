from fastapi import FastAPI

from api.routes.chat_routes import router

from database.db_engine import engine, SessionLocal
from database.models import Base, Customer

from utils.data_generator import generate_data


app = FastAPI()

# ALWAYS CREATE TABLES (Safe operation)
Base.metadata.create_all(bind=engine)


# SEED DATA ONLY IF EMPTY
def initialize_database():

    db = SessionLocal()

    try:
        customer_count = db.query(Customer).count()

        if customer_count == 0:
            print("🔥 EMPTY DATABASE DETECTED → GENERATING SAMPLE DATA")
            generate_data()
        else:
            print(f"✅ DATABASE READY → {customer_count} customers loaded")

    finally:
        db.close()


# RUN ON STARTUP
initialize_database()


# REGISTER ROUTES
app.include_router(router)
