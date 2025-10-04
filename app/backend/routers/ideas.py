from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
import json, random

from app.backend.db import get_db
from app.backend import models, schemas, auth

router = APIRouter(tags=["ideas"])

# --- OAuth2 scheme to get token from Authorization header ---
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


# --- Allowed categories ---
ALLOWED_CATEGORIES = [
    "home",
    "outdoor",
    "indoor",
    "artsy",
    "sports",
    "party",
    "drinking",
    "extra-romantic",
    "food",
    "on-a-budget",
    "culture",
    "self-care",
    "learning",
]


@router.get("/categories")
def list_categories():
    return {"categories": ALLOWED_CATEGORIES}


# --- CREATE IDEA ---
@router.post("/", response_model=schemas.IdeaOut, status_code=201)
def create_idea(
    payload: schemas.IdeaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not payload.categories or len(payload.categories) == 0:
        raise HTTPException(status_code=400, detail="Must select at least one category")
    if len(payload.categories) > 3:
        raise HTTPException(status_code=400, detail="Max 3 categories allowed")
    for cat in payload.categories:
        if cat not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Invalid category: {cat}")

    if "home" in payload.categories:
        payload.lat = None
        payload.lon = None

    idea = models.Idea(
        owner_id=current_user.id,
        title=payload.title,
        note=payload.note,
        categories=json.dumps(payload.categories),
        is_public=payload.is_public,
        is_home=payload.is_home,
        lat=payload.lat,
        lon=payload.lon,
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)

    return schemas.IdeaOut(
        id=idea.id,
        owner_id=idea.owner_id,
        title=idea.title,
        note=idea.note,
        categories=payload.categories,
        is_public=idea.is_public,
        is_home=idea.is_home,
        lat=idea.lat,
        lon=idea.lon,
    )


# --- EDIT IDEA ---
@router.put("/{idea_id}", response_model=schemas.IdeaOut)
def edit_idea(
    idea_id: int,
    payload: schemas.IdeaUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = db.query(models.Idea).get(idea_id)
    if not idea or idea.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Idea not found or not yours")

    if not payload.categories or len(payload.categories) == 0:
        raise HTTPException(status_code=400, detail="Must select at least one category")
    if len(payload.categories) > 3:
        raise HTTPException(status_code=400, detail="Max 3 categories allowed")

    if "home" in payload.categories:
        payload.lat = None
        payload.lon = None

    idea.title = payload.title
    idea.note = payload.note
    idea.categories = json.dumps(payload.categories)
    idea.is_public = payload.is_public
    idea.is_home = payload.is_home
    idea.lat = payload.lat
    idea.lon = payload.lon

    db.commit()
    db.refresh(idea)

    return schemas.IdeaOut(
        id=idea.id,
        owner_id=idea.owner_id,
        title=idea.title,
        note=idea.note,
        categories=payload.categories,
        is_public=idea.is_public,
        is_home=idea.is_home,
        lat=idea.lat,
        lon=idea.lon,
    )


# --- DELETE IDEA ---
@router.delete("/{idea_id}", status_code=204)
def delete_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = db.query(models.Idea).get(idea_id)
    if not idea or idea.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Idea not found or not yours")

    db.delete(idea)
    db.commit()
    return


# -------- HEART IDEA --------
@router.post("/heart/{idea_id}")
def heart_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = db.query(models.Idea).get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    if idea in current_user.favorites:
        return {"message": "Already in your jar"}

    current_user.favorites.append(idea)
    db.commit()
    return {"message": "Idea added to your jar"}


# -------- UNHEART IDEA --------
@router.delete("/heart/{idea_id}")
def unheart_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = db.query(models.Idea).get(idea_id)
    if not idea or idea not in current_user.favorites:
        raise HTTPException(status_code=404, detail="Not in your jar")

    current_user.favorites.remove(idea)
    db.commit()
    return {"message": "Idea removed from your jar"}


# --- MY JAR (own + favorites) ---
@router.get("/jar", response_model=List[schemas.IdeaOut])
def my_jar(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    own = db.query(models.Idea).filter(models.Idea.owner_id == current_user.id).all()
    hearted = current_user.favorites  # many-to-many relationship

    rows = own + hearted
    return [
        schemas.IdeaOut(
            id=r.id,
            owner_id=r.owner_id,
            title=r.title,
            note=r.note,
            categories=json.loads(r.categories) if r.categories else [],
            is_public=r.is_public,
            is_home=r.is_home,
            lat=r.lat,
            lon=r.lon,
        )
        for r in rows
    ]


# --- PUBLIC IDEAS ---
@router.get("/public", response_model=List[schemas.IdeaOut])
def public_ideas(category: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Idea).filter(models.Idea.is_public == True)

    rows = query.all()
    results = []

    for r in rows:
        cats = json.loads(r.categories) if r.categories else []
        # If a category is specified, skip those that don't include it
        if category and category not in cats:
            continue
        results.append(
            schemas.IdeaOut(
                id=r.id,
                owner_id=r.owner_id,
                title=r.title,
                note=r.note,
                categories=cats,
                is_public=r.is_public,
                is_home=r.is_home,
                lat=r.lat,
                lon=r.lon,
            )
        )
    return results


# --- RANDOM IDEA ---
@router.get("/random", response_model=schemas.IdeaOut)
def randomizer(
    category: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    own = db.query(models.Idea).filter(models.Idea.owner_id == current_user.id).all()
    hearted = current_user.favorites

    jar = own + hearted
    filtered = [
        i for i in jar if category in (json.loads(i.categories) if i.categories else [])
    ]
    if not filtered:
        raise HTTPException(status_code=404, detail="No ideas in this category")

    idea = random.choice(filtered)
    return schemas.IdeaOut(
        id=idea.id,
        owner_id=idea.owner_id,
        title=idea.title,
        note=idea.note,
        categories=json.loads(idea.categories) if idea.categories else [],
        is_public=idea.is_public,
        is_home=idea.is_home,
        lat=idea.lat,
        lon=idea.lon,
    )
