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

    current_user.favorites.append(idea)
    db.commit()

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


# -------- UNHEART IDEA (works for both own & hearted) --------
@router.delete("/heart/{idea_id}")
def unheart_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    idea = db.query(models.Idea).get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # --- If user owns the idea ---
    if idea.owner_id == current_user.id:
        # If it's public → remove from favorites only (keep in public list)
        if idea.is_public:
            if idea in current_user.favorites:
                current_user.favorites.remove(idea)
                db.commit()
            return {
                "message": "Removed public idea from your jar, still visible to others"
            }

        # If it's private → delete completely
        db.delete(idea)
        db.commit()
        return {"message": "Private idea deleted from your jar"}

    # --- If it's a hearted (not owned) idea ---
    if idea in current_user.favorites:
        current_user.favorites.remove(idea)
        db.commit()
        return {"message": "Idea removed from your jar"}

    # --- Otherwise not in jar ---
    raise HTTPException(status_code=404, detail="Idea not in your jar")


# --- MY JAR (own + favorites) ---
@router.get("/jar", response_model=List[schemas.IdeaOut])
def my_jar(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Get all user's ideas
    own = db.query(models.Idea).filter(models.Idea.owner_id == current_user.id).all()
    hearted = current_user.favorites  # many-to-many relationship

    # Remove public ideas the user owns (so they appear only if still hearted)
    visible_own = [idea for idea in own if not idea.is_public]

    rows = visible_own + hearted
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


@router.get("/random", response_model=schemas.IdeaOut)
def randomizer(
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    own = db.query(models.Idea).filter(models.Idea.owner_id == current_user.id).all()
    hearted = current_user.favorites

    jar = own + hearted
    if category:
        filtered = [
            i
            for i in jar
            if category in (json.loads(i.categories) if i.categories else [])
        ]
    else:
        filtered = jar  # ← if no category selected, use all ideas

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
