from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# ----------------------------------------
# Password Hashing
# ----------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if len(password) > 72:
        raise ValueError("password too long (max 72 characters for bcrypt)")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password using bcrypt."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------------------
# JWT Configuration
# ----------------------------------------

# Use environment variable OR fallback to a dev value
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.
    data: {"sub": user_id}
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.
    Returns payload dict if valid, else None.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
