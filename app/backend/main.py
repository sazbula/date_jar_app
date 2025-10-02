from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.backend.db import Base, engine
from app.backend.routers import ideas, users

# fastapi instance
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent  # DATE_JAR_APP/app/
FRONTEND_DIR = BASE_DIR / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# routers
app.include_router(users.router)
app.include_router(ideas.router)


# make tables when app starts
Base.metadata.create_all(bind=engine)
