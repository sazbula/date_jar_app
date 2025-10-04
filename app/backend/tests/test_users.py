def test_register_user(client):
    """
    Test that a new user can register successfully.
    """
    response = client.post(
        "/api/users/register", json={"username": "alice", "password": "secret123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_register_duplicate_user(client):
    """
    Test that registering with an existing username returns an error.
    """
    # Register first time
    client.post(
        "/api/users/register", json={"username": "bob", "password": "secret123"}
    )

    # Try again with same username
    response = client.post(
        "/api/users/register", json={"username": "bob", "password": "newpassword"}
    )
    assert response.status_code == 400
    assert "Username already taken" in response.text


def test_login_user_success(client):
    """
    Test that a registered user can log in and receive a JWT token.
    """
    # Register
    client.post(
        "/api/users/register", json={"username": "charlie", "password": "secret123"}
    )

    # Login
    response = client.post(
        "/api/users/login", json={"username": "charlie", "password": "secret123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(client):
    """
    Test that login fails with wrong username or password.
    """
    # Register
    client.post(
        "/api/users/register", json={"username": "diana", "password": "secret123"}
    )

    # Try wrong password
    wrong_pass = client.post(
        "/api/users/login", json={"username": "diana", "password": "wrongpass"}
    )
    assert wrong_pass.status_code == 401
    assert "Invalid username or password" in wrong_pass.text

    # Try non-existent user
    no_user = client.post(
        "/api/users/login", json={"username": "ghost", "password": "secret123"}
    )
    assert no_user.status_code == 401
    assert "Invalid username or password" in no_user.text
