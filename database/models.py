from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database.db_engine import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    persona = Column(String)
    preferred_channel = Column(String)
    churn_risk = Column(Float)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_name = Column(String)
    amount = Column(Float)
    channel = Column(String)


class EngagementEvent(Base):
    __tablename__ = "engagement_events"

    event_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    event_type = Column(String)
    channel = Column(String)
