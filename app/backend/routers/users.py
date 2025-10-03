from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.db import get_db
from app.backend import models, schemas, auth

router = APIRouter(tags=["users"])


# -------- REGISTER --------
@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models.User(
        username=payload.username,
        password_hash=auth.hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------- LOGIN (JSON, not form-data) --------
@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},  # store user.id inside token
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
