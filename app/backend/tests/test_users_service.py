from app.backend.services import users_service
from app.backend.db import Base
from app.backend.models import User


def test_register_user_success(client):
    payload = {"username": "bob", "password": "pass123"}
    r = client.post("/api/users/register", json=payload)
    assert r.status_code == 201
    assert r.json()["username"] == "bob"


def test_register_user_duplicate(client):
    # first create
    client.post("/api/users/register", json={"username": "kate", "password": "test"})

    # duplicate
    r = client.post(
        "/api/users/register", json={"username": "kate", "password": "test"}
    )
    assert r.status_code == 400


def test_login_success(client):
    client.post("/api/users/register", json={"username": "john", "password": "abc123"})
    r = client.post("/api/users/login", json={"username": "john", "password": "abc123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_invalid(client):
    r = client.post("/api/users/login", json={"username": "ghost", "password": "nope"})
    assert r.status_code == 401
