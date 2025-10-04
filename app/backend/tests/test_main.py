def test_health_route(client):
    """
    Test that the /api/health route is reachable and returns the correct status.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}
