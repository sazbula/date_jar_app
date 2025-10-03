from pydantic import BaseModel, Field, conlist
from typing import Optional, Annotated
from typing import List, Optional

# user schemas


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# idea schemas


class IdeaBase(BaseModel):
    title: str
    note: str = ""
    categories: list[str]
    is_public: bool = False
    is_home: bool = False
    address: Optional[str] = None
    lat: float | None = None
    lon: float | None = None


class IdeaCreate(IdeaBase):
    pass


class IdeaUpdate(IdeaBase):
    pass


class IdeaOut(IdeaBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


# favorite schemas


class FavoriteOut(BaseModel):
    user_id: int
    idea_id: int

    class Config:
        from_attributes = True
