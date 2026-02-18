from database.db_engine import engine
from database.models import Base

Base.metadata.create_all(bind=engine)

print("Database Initialized")
