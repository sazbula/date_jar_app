from pydantic import BaseModel
from typing import Optional, List


# -------- USER --------
class UserCreate(BaseModel):
    username: str
    password: str  # plain password, will be hashed before storing


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # works with SQLAlchemy ORM objects


# -------- TOKEN (for JWT login) --------
class Token(BaseModel):
    access_token: str
    token_type: str


# -------- IDEA --------
class IdeaBase(BaseModel):
    title: str
    note: str = ""
    categories: List[str]  # list instead of CSV (we’ll join/split in models)
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

    class Config:
        from_attributes = True


# -------- FAVORITE --------
class FavoriteOut(BaseModel):
    user_id: int
    idea_id: int

    class Config:
        from_attributes = True


# -------- TOKEN (for JWT login) --------
class Token(BaseModel):
    access_token: str
    token_type: str
