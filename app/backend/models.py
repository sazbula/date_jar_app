from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base


# the table for users in the database
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    # password (hashed)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # user relationships w ideas and favorites
    ideas = relationship("Idea", back_populates="owner", cascade="all, delete-orphan")


# the table for ideas in the db


class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    note: Mapped[str] = mapped_column(Text, default="")

    categories_json: Mapped[str] = mapped_column(Text, default="[]")

    # visibility
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_home: Mapped[bool] = mapped_column(Boolean, default=False)

    # coordinates (lat/lon for map)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    # relationships
    owner = relationship("User", back_populates="ideas")
    favorited_by = relationship(
        "Favorite", back_populates="idea", cascade="all, delete-orphan"
    )


# the table for favorites in the db (many-to-many relationship between users and ideas)
class Favorite(Base):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    idea_id: Mapped[int] = mapped_column(
        ForeignKey("ideas.id", ondelete="CASCADE"), primary_key=True
    )

    user = relationship("User")
    idea = relationship("Idea", back_populates="favorited_by")

    __table_args__ = (UniqueConstraint("user_id", "idea_id", name="uq_user_idea"),)
