"""
FastAPI Backend Application for Student Internship & Job Opportunity Platform.
Course: CSE309 Autumn 2026 Mid Project Assessment (MVP).
Architecture: Clean layered architecture with separated routers, models, database, and CRUD/service layers.
Compatible with Local, Docker, and Vercel serverless environments.
"""

import sys
from pathlib import Path

# Ensure backend directory and project root are in sys.path
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

try:
    from database import init_db
    from routers.health import router as health_router
    from routers.internships import router as internships_router
    from routers.auth import router as auth_router
    from routers.groups import router as groups_router
    from routers.admin import router as admin_router
except ImportError:
    from backend.database import init_db
    from backend.routers.health import router as health_router
    from backend.routers.internships import router as internships_router
    from backend.routers.auth import router as auth_router
    from backend.routers.groups import router as groups_router
    from backend.routers.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed initial records on startup
    init_db()
    yield


app = FastAPI(
    title="Student Internship & Job Opportunity Platform API",
    description="RESTful API implementing full CRUD operations for Internship Opportunities (CSE309 MVP)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# SWAGGER & OPENAPI DOCS (DUAL PREFIX FOR VERCEL & LOCAL COMPATIBILITY)
# =====================================================================

@app.get("/api/docs", include_in_schema=False)
def api_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - Swagger UI",
    )


@app.get("/api/redoc", include_in_schema=False)
def api_redoc_ui():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - ReDoc",
    )


@app.get("/api/openapi.json", include_in_schema=False)
def api_openapi():
    return JSONResponse(
        get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
            description=app.description,
        )
    )


# =====================================================================
# ROUTER REGISTRATION
# =====================================================================

# Mount routers under both "/api" and root "" prefixes for Vercel rewrite & local compatibility
app.include_router(health_router, prefix="/api")
app.include_router(health_router, prefix="")

app.include_router(internships_router, prefix="/api")
app.include_router(internships_router, prefix="")

app.include_router(auth_router, prefix="/api")
app.include_router(auth_router, prefix="")

app.include_router(groups_router, prefix="/api")
app.include_router(groups_router, prefix="")

app.include_router(admin_router, prefix="/api")
app.include_router(admin_router, prefix="")


# =====================================================================
# FRONTEND STATIC FILES (Production / Vercel Serving)
# =====================================================================

FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"

if FRONTEND_DIST_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST_DIR), html=True), name="frontend")
