from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.db import get_db
from app.backend.models import User
from app.backend.schemas import UserCreate, UserOut
from app.backend.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])


# registration and hash pass


@router.post("/register", status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    return {"message": f"User '{new_user.username}' registered successfully"}


# login
@router.post("/login")
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": f"Login successful! Welcome {user.username}"}


# heart an idea
@router.post("/heart/{idea_id}")
def heart_idea(idea_id: int, creds: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == creds.username).first()
    if not user or not verify_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    idea = db.query(Idea).get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # already hearted before
    existing = db.query(Favorite).filter_by(user_id=user.id, idea_id=idea.id).first()
    if existing:
        return {"message": "Already in your jar"}

    fav = Favorite(user_id=user.id, idea_id=idea.id)
    db.add(fav)
    db.commit()
    return {"message": "Idea added to your jar"}


# unheart
@router.delete("/heart/{idea_id}")
def unheart_idea(idea_id: int, creds: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == creds.username).first()
    if not user or not verify_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    fav = db.query(Favorite).filter_by(user_id=user.id, idea_id=idea_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Not in your jar")

    db.delete(fav)
    db.commit()
    return {"message": "Idea removed from your jar"}
