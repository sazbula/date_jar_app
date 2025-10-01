# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db


# Create a TEST database engine (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory bound to the test engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 3. Dependency override for get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 4. Apply the override so the app uses the test DB
app.dependency_overrides[get_db] = override_get_db


#  5. Create tables for all models before tests run
Base.metadata.create_all(bind=engine)


# 6. Define pytest fixtures


@pytest.fixture(scope="module")
def client():
    """
    Fixture that provides a TestClient for the FastAPI app.
    Uses the in-memory SQLite database instead of the real one.
    """
    return TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a fresh database session for each test.
    Rolls back changes after each test for isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
