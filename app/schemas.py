from pydantic import BaseModel, Field
from typing import List, Optional

# user schemas


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# idea schemas


class IdeaBase(BaseModel):
    title: str
    note: str = ""
    categories: List[str] = []
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


# favorite schemas


class FavoriteOut(BaseModel):
    user_id: int
    idea_id: int

    class Config:
        from_attributes = True
