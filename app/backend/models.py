from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from app.backend.db import Base

# Association table: user favorites an idea
favorites_table = Table(
    "favorites",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("idea_id", ForeignKey("ideas.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, index=True)
    password_hash: str = Column(String(200))  # hashed password only

    # One-to-many: user → ideas
    ideas: List["Idea"] = relationship("Idea", back_populates="owner")

    # Many-to-many: user ↔ ideas (favorites)
    favorites: List["Idea"] = relationship(
        "Idea",
        secondary=favorites_table,
        back_populates="favorited_by",
    )


class Idea(Base):
    __tablename__ = "ideas"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(200), index=True)
    note: str = Column(String(500), default="")
    categories: str = Column(String)  # stored as JSON string
    is_public: bool = Column(Boolean, default=False)
    is_home: bool = Column(Boolean, default=False)
    lat: float | None = Column(Float, nullable=True)
    lon: float | None = Column(Float, nullable=True)

    # Foreign key
    owner_id: int = Column(Integer, ForeignKey("users.id"))

    # Reverse relationship
    owner: "User" = relationship("User", back_populates="ideas")

    # Many-to-many reverse: idea ↔ users
    favorited_by: List["User"] = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorites",
    )
