from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.backend.db import get_db
from app.backend import models, schemas, auth
from app.backend.services import ideas_service

router = APIRouter(tags=["ideas"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    payload = auth.decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --- Category list ---
@router.get("/categories")
def list_categories():
    return {"categories": ideas_service.ALLOWED_CATEGORIES}


# --- Create idea ---
@router.post("/", response_model=schemas.IdeaOut, status_code=201)
def create_idea(
    payload: schemas.IdeaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = ideas_service.create_idea(db, current_user, payload)
    return schemas.idea_to_out(idea)


# --- Add to jar ---
@router.post("/heart/{idea_id}")
def heart_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return ideas_service.heart_idea(db, current_user, idea_id)


# --- Remove from jar / delete ---
@router.delete("/heart/{idea_id}")
def unheart_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return ideas_service.unheart_idea(db, current_user, idea_id)


# --- My jar ---
@router.get("/jar", response_model=List[schemas.IdeaOut])
def my_jar(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ideas = ideas_service.get_user_jar(db, current_user)
    return [schemas.idea_to_out(i) for i in ideas]


# --- Public ideas ---
@router.get("/public", response_model=List[schemas.IdeaOut])
def public_ideas(
    category: str | None = None,
    db: Session = Depends(get_db),
):
    ideas = ideas_service.get_public_ideas(db, category)
    return [schemas.idea_to_out(i) for i in ideas]


# --- Random idea ---
@router.get("/random", response_model=schemas.IdeaOut)
def randomizer(
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = ideas_service.random_idea(db, current_user, category)
    return schemas.idea_to_out(idea)
