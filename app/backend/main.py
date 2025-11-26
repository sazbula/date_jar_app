from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.backend.routers import users, ideas
from app.backend.db import Base, engine, TESTING

app = FastAPI(title="Date Jar API")


# ------------------------------------
# CREATE TABLES IF RUNNING THE SERVER
# ------------------------------------
if not TESTING:
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
else:
    print("TESTING mode: NOT creating tables or connecting to Postgres")


# ------------------------------------
# SERVE FRONTEND FILES
# ------------------------------------
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")


@app.get("/")
def serve_login():
    return FileResponse("app/frontend/login.html")


@app.get("/public")
def serve_public():
    return FileResponse("app/frontend/public.html")


@app.get("/add")
def serve_add():
    return FileResponse("app/frontend/add.html")


@app.get("/jar")
def serve_jar():
    return FileResponse("app/frontend/jar.html")


@app.get("/map")
def serve_map():
    return FileResponse("app/frontend/map.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="Date Jar API",
        version="1.0.0",
        description="API for Date Jar App",
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])

Instrumentator().instrument(app).expose(app)
