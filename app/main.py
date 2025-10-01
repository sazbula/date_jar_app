from fastapi import FastAPI
from .db import Base, engine
from fastapi.staticfiles import StaticFiles


from .routers import users, ideas

# fastapi instance
app = FastAPI()


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# routers
app.include_router(users.router)
app.include_router(ideas.router)


# make tables when app starts
Base.metadata.create_all(bind=engine)
