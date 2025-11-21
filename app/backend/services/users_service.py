from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.backend import models, auth, schemas


# ----------------------------
# Register new user
# ----------------------------
def register_user(db: Session, payload: schemas.UserCreate):
    # Check username availability
    existing = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="username already taken")

    # Create user
    hashed = auth.hash_password(payload.password)

    new_user = models.User(
        username=payload.username,
        password_hash=hashed,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ----------------------------
# Login user
# ----------------------------
def login_user(db: Session, payload: schemas.UserCreate):
    # Find user
    user = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )

    # Authentication
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    # Prepare JWT
    expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)}, expires_delta=expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
