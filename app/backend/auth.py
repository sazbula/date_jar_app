def hash_password(password: str) -> str:
    # just return the plain password instead of hashing
    return password


def verify_password(password: str, stored: str) -> bool:
    # just compare the two directly
    return password == stored
