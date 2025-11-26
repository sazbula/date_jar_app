from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ---------------------------------------------------
# DATABASE URL
# ---------------------------------------------------
# Reads from Azure App Settings (DATABASE_URL)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/datejar"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session local factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for ORM models
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
# Manual DB initialization (optional local use)
# ---------------------------------------------------
def init_db():
    """
    Initialize database tables (local development use).
    In Azure, tables are created automatically on startup.
    """
    from app.backend import models

    Base.metadata.create_all(bind=engine)
