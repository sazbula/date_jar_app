def test_list_categories(client):
    r = client.get("/api/ideas/categories")
    assert r.status_code == 200
    assert "categories" in r.json()


def test_create_idea(client, auth_header):
    payload = {
        "title": "Picnic",
        "note": "In the park",
        "categories": ["outdoor"],
        "is_public": False,
        "is_home": False,
        "lat": 10.0,
        "lon": 20.0,
    }

    r = client.post("/api/ideas/", json=payload, headers=auth_header)
    assert r.status_code == 201
    assert r.json()["title"] == "Picnic"


def test_public_ideas(client, auth_header):
    # Create idea
    payload = {
        "title": "Museum",
        "note": "Art",
        "categories": ["culture"],
        "is_public": True,
        "is_home": False,
    }
    client.post("/api/ideas/", json=payload, headers=auth_header)

    r = client.get("/api/ideas/public")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_random_idea(client, auth_header):
    r = client.get("/api/ideas/random", headers=auth_header)
    assert r.status_code in (200, 404)
