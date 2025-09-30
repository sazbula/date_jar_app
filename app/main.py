from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db import Base, engine


# Create a FastAPI app instance
app = FastAPI()

# Mount the frontend folder at root url
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# simple API endpoint at /api/health, returns status ok in json format
@app.get("/api/health")
def health():
    return {"status": "ok"}


# make tables when app starts
Base.metadata.create_all(bind=engine)
