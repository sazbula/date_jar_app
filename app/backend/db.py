# db.py → here i connect the app to the SQLite database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# where the database lives
DATABASE_URL = "sqlite:///./datejar.db"

# drives the connection to the database.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# starting point for all of all things(User, Idea, Favorite)
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
