def test_register_route(client):
    payload = {"username": "maria", "password": "pw123"}
    r = client.post("/api/users/register", json=payload)
    assert r.status_code == 201
    assert r.json()["username"] == "maria"


def test_login_route(client):
    client.post("/api/users/register", json={"username": "tim", "password": "pass"})
    r = client.post("/api/users/login", json={"username": "tim", "password": "pass"})
    assert r.status_code == 200
    assert "access_token" in r.json()
