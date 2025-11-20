from pydantic import BaseModel
from typing import Optional, List
import json


# User Schemas


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# Token Schema (JWT)


class Token(BaseModel):
    access_token: str
    token_type: str


# Idea Schemas


class IdeaBase(BaseModel):
    title: str
    note: str = ""
    categories: List[str]
    is_public: bool = False
    is_home: bool = False
    lat: Optional[float] = None
    lon: Optional[float] = None


class IdeaCreate(IdeaBase):
    pass


class IdeaUpdate(IdeaBase):
    pass


class IdeaOut(IdeaBase):
    id: int
    owner_id: int
    owner_username: Optional[str] = None

    class Config:
        from_attributes = True


# Favorite Schema


class FavoriteOut(BaseModel):
    user_id: int
    idea_id: int

    class Config:
        from_attributes = True


# Conversion Helpers


def idea_to_out(model):
    """
    Convert SQLAlchemy Idea model -> IdeaOut schema.
    Keeps routers and services clean.
    """
    return IdeaOut(
        id=model.id,
        owner_id=model.owner_id,
        owner_username=getattr(model.owner, "username", None),
        title=model.title,
        note=model.note,
        categories=json.loads(model.categories) if model.categories else [],
        is_public=model.is_public,
        is_home=model.is_home,
        lat=model.lat,
        lon=model.lon,
    )
