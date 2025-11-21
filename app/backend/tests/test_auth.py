from app.backend import auth


def test_hash_and_verify_password():
    pwd = "secret123"
    hashed = auth.hash_password(pwd)

    assert auth.verify_password(pwd, hashed) is True
    assert auth.verify_password("wrong", hashed) is False


def test_jwt_create_and_decode():
    token = auth.create_access_token({"sub": "5"})
    decoded = auth.decode_access_token(token)

    assert decoded is not None
    assert decoded["sub"] == "5"
