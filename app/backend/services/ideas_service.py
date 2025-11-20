import json, random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.backend import models


# ----------------------------
# Allowed Categories
# ----------------------------
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


# ----------------------------
# Validation
# ----------------------------
def validate_categories(categories: list[str]):
    if not categories:
        raise HTTPException(status_code=400, detail="Must select at least one category")
    if len(categories) > 3:
        raise HTTPException(status_code=400, detail="Max 3 categories allowed")
    for cat in categories:
        if cat not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Invalid category: {cat}")


# ----------------------------
# Create Idea
# ----------------------------
def create_idea(db: Session, user: models.User, payload):
    validate_categories(payload.categories)

    # Coordinates: remove if "home"
    lat = None
    lon = None
    if "home" not in payload.categories:
        lat = payload.lat
        lon = payload.lon

    idea = models.Idea(
        owner_id=user.id,
        title=payload.title,
        note=payload.note,
        categories=json.dumps(payload.categories),
        is_public=payload.is_public,
        is_home=payload.is_home,
        lat=lat,
        lon=lon,
    )

    db.add(idea)
    db.commit()
    db.refresh(idea)

    # Auto-favorite
    user.favorites.append(idea)
    db.commit()

    return idea


# ----------------------------
# Heart Idea
# ----------------------------
def heart_idea(db: Session, user: models.User, idea_id: int):
    idea = db.query(models.Idea).get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    if idea in user.favorites:
        return {"message": "Already in your jar"}

    user.favorites.append(idea)
    db.commit()
    return {"message": "Idea added to your jar"}


# ----------------------------
# Unheart/Delete Idea
# ----------------------------
def unheart_idea(db: Session, user: models.User, idea_id: int):
    idea = db.query(models.Idea).get(idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    # If user owns the idea
    if idea.owner_id == user.id:
        # Public ideas: remove from favorites but keep in public
        if idea.is_public:
            if idea in user.favorites:
                user.favorites.remove(idea)
                db.commit()
            return {"message": "Removed public idea from jar, still public"}

        # Private ideas: delete entirely
        db.delete(idea)
        db.commit()
        return {"message": "Private idea deleted"}

    # If user had hearted the idea
    if idea in user.favorites:
        user.favorites.remove(idea)
        db.commit()
        return {"message": "Idea removed from your jar"}

    raise HTTPException(status_code=404, detail="Idea not in your jar")


# ----------------------------
# User Jar (owned + hearted)
# ----------------------------
def get_user_jar(db: Session, user: models.User):
    own = db.query(models.Idea).filter(models.Idea.owner_id == user.id).all()
    hearted = user.favorites

    # Hide public ideas (they are in /public)
    visible_own = [idea for idea in own if not idea.is_public]

    return visible_own + list(hearted)


# ----------------------------
# Public Ideas
# ----------------------------
def get_public_ideas(db: Session, category: str | None):
    rows = db.query(models.Idea).filter(models.Idea.is_public == True).all()

    if category:
        return [
            idea
            for idea in rows
            if category in (json.loads(idea.categories) if idea.categories else [])
        ]

    return rows


# ----------------------------
# Random Idea
# ----------------------------
def random_idea(db: Session, user: models.User, category: str | None):
    own = db.query(models.Idea).filter(models.Idea.owner_id == user.id).all()
    hearted = user.favorites

    jar = own + list(hearted)

    if category:
        jar = [
            idea
            for idea in jar
            if category in (json.loads(idea.categories) if idea.categories else [])
        ]

    if not jar:
        raise HTTPException(status_code=404, detail="No ideas in this category")

    return random.choice(jar)
