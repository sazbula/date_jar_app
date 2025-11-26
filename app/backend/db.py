from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/datejar"
)

engine = create_engine(DATABASE_URL)
# If i ever use password:
# SQLALCHEMY_DATABASE_URL = "postgresql://sabinabacaoanu:YOUR_PASSWORD@localhost:5432/datejar"


# Session = handle DB connection per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


# ---------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------
# DB initialization
# ---------------------------------------------------
def init_db():
    """
    Initialize the database tables.
    Call this manually (python shell).
    """

    from app.backend import models

    Base.metadata.create_all(bind=engine)
