from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------

# If Postgres user has no password
SQLALCHEMY_DATABASE_URL = "postgresql://sabinabacaoanu@localhost:5432/datejar"

# If i ever use password:
# SQLALCHEMY_DATABASE_URL = "postgresql://sabinabacaoanu:YOUR_PASSWORD@localhost:5432/datejar"


# Important: enable psycopg properly
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=False,
)

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
