from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./datejar.db"

# Engine = actual DB connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session = talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class = all models will inherit from this
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  DB initialization function
def init_db():
    """
    Initialize the database tables.
    Must be called manually — NOT from main.py.
    """
    # Import models inside the function so Base knows them
    from app.backend import models

    Base.metadata.create_all(bind=engine)
