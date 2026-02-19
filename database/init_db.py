from database.db_engine import engine, Base
from database import models   # VERY IMPORTANT → registers tables

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully")
