from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from app.backend.db import Base

# Association table
favorites_table = Table(
    "favorites",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("idea_id", ForeignKey("ideas.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True  # ⭐ FIX

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(200))

    ideas = relationship("Idea", back_populates="owner")
    favorites = relationship(
        "Idea",
        secondary=favorites_table,
        back_populates="favorited_by",
    )


class Idea(Base):
    __tablename__ = "ideas"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    note = Column(String(500), default="")
    categories = Column(String)
    is_public = Column(Boolean, default=False)
    is_home = Column(Boolean, default=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="ideas")

    favorited_by = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorites",
    )
