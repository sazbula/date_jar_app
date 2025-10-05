from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash a new password when registering
def hash_password(password: str) -> str:
    # bcrypt only accepts up to 72 characters
    print("DEBUG password length:", len(password), "value:", password[:100])
    if len(password) > 72:
        raise ValueError("password too long (max 72 characters for bcrypt)")
    return pwd_context.hash(password)


# verify password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# jwt configuration
SECRET_KEY = "supersecretkey"  # todo: replace with env var later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day


# create a signed jwt token with expiration
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# decode and validate a jwt token
def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
