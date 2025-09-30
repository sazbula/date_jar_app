# auth.py → handles password hashing and checking
from passlib.context import CryptContext

# bcrypt = secure hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:

    return pwd_context.verify(password, hashed)
