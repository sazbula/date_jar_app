from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db import Base, engine
from .db import Base, engine
from . import models


# fastapi instance
app = FastAPI()


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# make tables when app starts
Base.metadata.create_all(bind=engine)
