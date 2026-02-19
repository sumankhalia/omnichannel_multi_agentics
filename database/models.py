from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db_engine import Base


# ---------------------------------------------------
# CUSTOMER TABLE
# ---------------------------------------------------

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    persona = Column(String)
    preferred_channel = Column(String)
    churn_risk = Column(Float)

    signup_date = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="customer")
    events = relationship("EngagementEvent", back_populates="customer")


# ---------------------------------------------------
# TRANSACTIONS TABLE
# ---------------------------------------------------

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))

    product_name = Column(String)
    amount = Column(Float)
    channel = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="transactions")


# ---------------------------------------------------
# ENGAGEMENT EVENTS TABLE
# ---------------------------------------------------

class EngagementEvent(Base):
    __tablename__ = "engagement_events"

    event_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))

    event_type = Column(String)
    channel = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="events")
