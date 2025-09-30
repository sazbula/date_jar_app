from fastapi import FastAPI, Depends, HTTPException
from .db import Base, engine, get_db
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .schemas import UserCreate
from .auth import hash_password, verify_password

# fastapi instance
app = FastAPI()


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/users/register", status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # username already exists
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # new user with hashed password
    new_user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    return {"message": f"User '{new_user.username}' registered successfully"}


@app.post("/users/login")
def login(payload: UserCreate, db: Session = Depends(get_db)):
    # find user by username
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # check password against hash
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Login successful! Welcome {user.username}"}


# make tables when app starts
Base.metadata.create_all(bind=engine)
