from database.db_engine import SessionLocal
from database.models import Customer

db = SessionLocal()

customers = db.query(Customer).limit(5).all()

for c in customers:
    print(c.name, c.churn_risk)

db.close()
