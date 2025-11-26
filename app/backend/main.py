from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.backend.routers import users, ideas
import os

app = FastAPI(title="Date Jar API")

# -------------------------------
# SERVE FRONTEND FILES
# -------------------------------

# Serve CSS/JS/image assets under /static
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")


# Serve actual HTML frontend pages
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


# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}


# -------------------------------
# OPENAPI CUSTOMIZATION
# -------------------------------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Date Jar API",
        version="1.0.0",
        description="API for Date Jar App",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# API ROUTERS
# -------------------------------
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])

# -------------------------------
# PROMETHEUS METRICS
# -------------------------------
Instrumentator().instrument(app).expose(app)
