import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.db import Base, get_db
from app.backend.main import app
from app.backend import models


# ----------------------------------------------------
# IN-MEMORY TEST DATABASE  (always clean)
# ----------------------------------------------------
TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Single shared connection for in-memory DB
connection = engine.connect()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=connection,
)

# Reset tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# ----------------------------------------------------
# Override dependency
# ----------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ----------------------------------------------------
# Client
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
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def auth_token(client, test_user):
    payload = {"username": "alice", "password": "test123"}
    r = client.post("/api/users/login", json=payload)
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
