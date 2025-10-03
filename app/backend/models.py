from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from app.backend.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # relationships
    ideas = relationship("Idea", back_populates="owner")
    favorites = relationship(
        "Idea", secondary="favorites", back_populates="favorited_by"
    )


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    note = Column(String, default="")
    categories = Column(String)
    is_public = Column(Boolean, default=False)
    is_home = Column(Boolean, default=False)
    lat = Column(Float)
    lon = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # relationships
    owner = relationship("User", back_populates="ideas")
    favorited_by = relationship(
        "User", secondary="favorites", back_populates="favorites"
    )


class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
