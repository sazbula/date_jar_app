from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.backend.db import Base, engine
from app.backend.routers import users, ideas
from fastapi.openapi.utils import get_openapi

# Create app
app = FastAPI(title="Date Jar API")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Date Jar API",
        version="1.0.0",
        description="API for Date Jar App",
        routes=app.routes,
    )
    # Define simple JWT bearer auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    # Apply it globally so all endpoints require it (unless overridden)
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS (allow frontend calls from file:// or localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])

# Init DB
Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}
