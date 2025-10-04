from datetime import timedelta
from app.backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def test_hash_and_verify_password():
    """Test password hashing and verification logic."""
    password = "supersecret123"
    hashed = hash_password(password)

    # Hash should not equal the plain password
    assert hashed != password

    # Verification should pass for correct password
    assert verify_password(password, hashed)

    # Verification should fail for incorrect password
    assert not verify_password("wrongpassword", hashed)


def test_create_and_decode_access_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "user1"}
    token = create_access_token(data)

    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user1"


def test_token_expiration():
    """Ensure token expires correctly when given a short lifespan."""
    data = {"sub": "user2"}
    short_expire = timedelta(seconds=-10)  # expired 10 seconds ago
    token = create_access_token(data, expires_delta=short_expire)

    decoded = decode_access_token(token)
    assert decoded is None  # Token should be invalid due to expiration
