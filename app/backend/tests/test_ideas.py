import json


# Utility to register + login user quickly
def register_and_login(client, username="user", password="pass123"):
    client.post(
        "/api/users/register", json={"username": username, "password": password}
    )
    res = client.post(
        "/api/users/login", json={"username": username, "password": password}
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_idea_success(client):
    """
    Test creating a valid idea with an authenticated user.
    """
    headers = register_and_login(client)

    idea_data = {
        "title": "Picnic at Retiro Park",
        "note": "Bring sandwiches and a blanket",
        "categories": ["outdoor", "food"],
        "is_public": True,
        "is_home": False,
        "lat": 40.415,
        "lon": -3.684,
    }

    response = client.post("/api/ideas/", json=idea_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Picnic at Retiro Park"
    assert "id" in data


def test_create_idea_requires_token(client):
    """
    Test that idea creation without a token fails.
    """
    idea_data = {
        "title": "Home movie night",
        "note": "Choose something cozy",
        "categories": ["home", "indoor"],
        "is_public": False,
        "is_home": True,
    }

    response = client.post("/api/ideas/", json=idea_data)
    assert response.status_code == 401


def test_invalid_categories(client):
    """
    Test idea creation fails with invalid categories.
    """
    headers = register_and_login(client)

    bad_idea = {
        "title": "Skydiving date",
        "note": "Extreme fun!",
        "categories": ["dangerous"],  # ❌ not allowed
        "is_public": True,
    }

    res = client.post("/api/ideas/", json=bad_idea, headers=headers)
    assert res.status_code == 400
    assert "Invalid category" in res.text


def test_public_ideas_listing(client):
    """
    Test that public ideas appear in /public route.
    """
    headers = register_and_login(client, username="publicUser")

    # Create a public idea
    client.post(
        "/api/ideas/",
        json={
            "title": "Art gallery visit",
            "note": "Museo Reina Sofia",
            "categories": ["culture", "artsy"],
            "is_public": True,
        },
        headers=headers,
    )

    res = client.get("/api/ideas/public")
    assert res.status_code == 200
    ideas = res.json()
    assert any("Art gallery visit" in i["title"] for i in ideas)


def test_heart_and_unheart_idea(client):
    """
    Test hearting and unhearting another user's idea.
    """
    # User A creates a public idea
    headers_a = register_and_login(client, username="A")
    create_res = client.post(
        "/api/ideas/",
        json={
            "title": "Cooking class",
            "note": "Learn Italian pasta",
            "categories": ["food", "learning"],
            "is_public": True,
        },
        headers=headers_a,
    )
    idea_id = create_res.json()["id"]

    # User B hearts it
    headers_b = register_and_login(client, username="B")
    heart_res = client.post(f"/api/ideas/heart/{idea_id}", headers=headers_b)
    assert heart_res.status_code == 200
    assert "added" in heart_res.json()["message"].lower()

    # User B unhearts it
    unheart_res = client.delete(f"/api/ideas/heart/{idea_id}", headers=headers_b)
    assert unheart_res.status_code == 200
    assert "removed" in unheart_res.json()["message"].lower()
