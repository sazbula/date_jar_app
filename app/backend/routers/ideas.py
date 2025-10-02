from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json, random
from ..backend.db import get_db
from ..backend.models import User, Idea, Favorite
from ..backend.schemas import UserCreate, IdeaCreate, IdeaUpdate, IdeaOut
from ..backend.auth import verify_password

router = APIRouter(prefix="/ideas", tags=["ideas"])


# to auth user
def authenticate(db: Session, creds: UserCreate) -> User | None:
    user = db.query(User).filter(User.username == creds.username).first()
    if user and verify_password(creds.password, user.password_hash):
        return user
    return None


# possible categories
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


# creating idea
@router.post("/", response_model=IdeaOut, status_code=201)
def create_idea(payload: IdeaCreate, creds: UserCreate, db: Session = Depends(get_db)):
    user = authenticate(db, creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # validate categories: must pick 1–3, all valid
    if not payload.categories or len(payload.categories) == 0:
        raise HTTPException(
            status_code=400, detail="You must select at least one category"
        )
    if len(payload.categories) > 3:
        raise HTTPException(
            status_code=400, detail="You can select a maximum of 3 categories"
        )
    for cat in payload.categories:
        if cat not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Invalid category: {cat}")

    # special handling for "home" ideas
    if "home" in payload.categories:
        payload.lat = None
        payload.lon = None

    idea = Idea(
        owner_id=user.id,
        title=payload.title,
        note=payload.note,
        categories_json=json.dumps(payload.categories),
        is_public=payload.is_public,
        is_home=payload.is_home,
        lat=payload.lat,
        lon=payload.lon,
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return IdeaOut(
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


# editing idea
@router.put("/{idea_id}", response_model=IdeaOut)
def edit_idea(
    idea_id: int, payload: IdeaUpdate, creds: UserCreate, db: Session = Depends(get_db)
):
    user = authenticate(db, creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # validate categories: must pick 1–3, all valid
    if not payload.categories or len(payload.categories) == 0:
        raise HTTPException(
            status_code=400, detail="You must select at least one category"
        )
    if len(payload.categories) > 3:
        raise HTTPException(
            status_code=400, detail="You can select a maximum of 3 categories"
        )
    for cat in payload.categories:
        if cat not in ALLOWED_CATEGORIES:
            raise HTTPException(status_code=400, detail=f"Invalid category: {cat}")

    # special handling for "home" ideas
    if "home" in payload.categories:
        payload.lat = None
        payload.lon = None

    idea = db.query(Idea).get(idea_id)
    if not idea or idea.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Idea not found or not yours")

    idea.title = payload.title
    idea.note = payload.note
    idea.categories_json = json.dumps(payload.categories)
    idea.is_public = payload.is_public
    idea.is_home = payload.is_home
    idea.lat = payload.lat
    idea.lon = payload.lon
    db.commit()
    db.refresh(idea)
    return IdeaOut(
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


# deleting idea
@router.delete("/{idea_id}", status_code=204)
def delete_idea(idea_id: int, creds: UserCreate, db: Session = Depends(get_db)):
    user = authenticate(db, creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    idea = db.query(Idea).get(idea_id)
    if not idea or idea.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Idea not found or not yours")

    db.delete(idea)
    db.commit()
    return


# my jar - private + hearted
@router.get("/jar", response_model=list[IdeaOut])
def my_jar(creds: UserCreate, db: Session = Depends(get_db)):
    user = authenticate(db, creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # my own
    own = db.query(Idea).filter(Idea.owner_id == user.id).all()
    # hearted
    favs = db.query(Favorite).filter(Favorite.user_id == user.id).all()
    hearted = [db.query(Idea).get(f.idea_id) for f in favs]

    rows = own + hearted
    return [
        IdeaOut(
            id=r.id,
            owner_id=r.owner_id,
            title=r.title,
            note=r.note,
            categories=json.loads(r.categories_json),
            is_public=r.is_public,
            is_home=r.is_home,
            lat=r.lat,
            lon=r.lon,
        )
        for r in rows
    ]


# looking at public ideas
@router.get("/public", response_model=list[IdeaOut])
def public_ideas(db: Session = Depends(get_db)):
    rows = db.query(Idea).filter(Idea.is_public == True).all()
    return [
        IdeaOut(
            id=r.id,
            owner_id=r.owner_id,
            title=r.title,
            note=r.note,
            categories=json.loads(r.categories_json),
            is_public=r.is_public,
            is_home=r.is_home,
            lat=r.lat,
            lon=r.lon,
        )
        for r in rows
    ]


# randomizer to pick idea from, using category
@router.get("/random", response_model=IdeaOut)
def randomizer(category: str, creds: UserCreate, db: Session = Depends(get_db)):
    user = authenticate(db, creds)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # all from personal jar
    own = db.query(Idea).filter(Idea.owner_id == user.id).all()
    favs = db.query(Favorite).filter(Favorite.user_id == user.id).all()
    hearted = [db.query(Idea).get(f.idea_id) for f in favs]
    jar = own + hearted

    # category
    filtered = [i for i in jar if category in json.loads(i.categories_json)]
    if not filtered:
        raise HTTPException(status_code=404, detail="No ideas in this category")

    idea = random.choice(filtered)
    return IdeaOut(
        id=idea.id,
        owner_id=idea.owner_id,
        title=idea.title,
        note=idea.note,
        categories=json.loads(idea.categories_json),
        is_public=idea.is_public,
        is_home=idea.is_home,
        lat=idea.lat,
        lon=idea.lon,
    )
