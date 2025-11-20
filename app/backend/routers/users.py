from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.backend.db import get_db
from app.backend import schemas
from app.backend.services import users_service

router = APIRouter(tags=["users"])


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return users_service.register_user(db, payload)


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return users_service.login_user(db, payload)
