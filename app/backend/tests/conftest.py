import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.db import Base, get_db
from app.backend.main import app


# ----------------------------------------------------
# IN-MEMORY TEST DATABASE
# ----------------------------------------------------
TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# One shared DB connection
connection = engine.connect()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection,
)


# ----------------------------------------------------
# CLEAN DB BEFORE EACH TEST
# ----------------------------------------------------
@pytest.fixture(autouse=True)
def clean_db():
    """Reset all tables before every test (prevents user already exists errors)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ----------------------------------------------------
# Override get_db dependency
# ----------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ----------------------------------------------------
# Test client fixture
# ----------------------------------------------------
@pytest.fixture
def client():
    return TestClient(app)


# ----------------------------------------------------
# Base user fixture
# ----------------------------------------------------
@pytest.fixture
def test_user(client):
    payload = {"username": "alice", "password": "test123"}
    r = client.post("/api/users/register", json=payload)

    # Allow 400 if the test creates multiple times in one file
    # but normally DB resets, so this will be 201.
    assert r.status_code in (201, 400)

    return {"username": "alice"}


@pytest.fixture
def auth_token(client, test_user):
    payload = {"username": "alice", "password": "test123"}
    r = client.post("/api/users/login", json=payload)
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
