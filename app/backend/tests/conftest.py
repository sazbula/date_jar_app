import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.main import app
from app.backend.db import Base, get_db

# --- 1. Create a temporary test database (SQLite) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# --- 2. Create a fixture that resets DB before each test ---
@pytest.fixture(scope="function")
def db_session():
    # Drop all tables and recreate them before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db  # this makes db available to the test
    finally:
        db.close()


# --- 3. Create a fixture that gives us a working test client ---
@pytest.fixture(scope="function")
def client(db_session):
    # Override FastAPI's get_db dependency so it uses our test DB
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Use FastAPI's built-in test client
    with TestClient(app) as c:
        yield c
