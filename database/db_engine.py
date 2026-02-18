import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# -----------------------------
# DATABASE URL
# -----------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

# FALLBACK
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./omni.db"

# -----------------------------
# ENGINE
# -----------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -----------------------------
# SESSION
# -----------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# DECLARATIVE BASE (CRITICAL)
# -----------------------------

Base = declarative_base()
