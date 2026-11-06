"""
FastAPI Backend Application for Student Internship & Job Opportunity Platform.
Course: CSE309 Autumn 2026 Mid Project Assessment (MVP).
Implements complete CRUD REST APIs for Internship Opportunity Management.
Designed for local, Docker, and Vercel serverless deployment.
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
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

try:
    from database import engine, get_session, init_db, SAMPLE_INTERNSHIPS
    from models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )
except ImportError:
    from backend.database import engine, get_session, init_db, SAMPLE_INTERNSHIPS
    from backend.models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )


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
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define an APIRouter so endpoints can be mounted at both "/api" and root ""
router = APIRouter()


# =====================================================================
# SYSTEM & HEALTH ENDPOINTS
# =====================================================================

@router.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "healthy",
        "service": "Student Internship & Job Opportunity Platform API",
        "version": "1.0.0"
    }


# =====================================================================
# 1. CREATE OPERATION (C in CRUD)
# =====================================================================

@router.post(
    "/internships",
    response_model=Internship,
    status_code=status.HTTP_201_CREATED,
    tags=["Internships"],
    summary="Create a new internship opportunity",
)
def create_internship(
    data: InternshipCreate,
    session: Session = Depends(get_session)
):
    """
    Creates a new internship record.
    - Validates payload using Pydantic/SQLModel
    - Generates unique UUID and creation timestamp
    - Persists record to the database
    - Returns HTTP 201 Created with the stored record
    """
    internship = Internship.model_validate(data)
    session.add(internship)
    session.commit()
    session.refresh(internship)
    return internship


# =====================================================================
# 2. READ LIST OPERATION (R in CRUD - All Records)
# =====================================================================

@router.get(
    "/internships",
    response_model=List[Internship],
    status_code=status.HTTP_200_OK,
    tags=["Internships"],
    summary="Get all internships with optional search and filter",
)
def get_internships(
    search: Optional[str] = Query(None, description="Search by title, company, or location"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: Open or Closed"),
    session: Session = Depends(get_session)
):
    """
    Retrieves all internship opportunities from the database.
    - Supports optional keyword search in title, company_name, and location
    - Supports optional status filtering (Open / Closed)
    - Returns sorted by created_at descending (newest first)
    """
    statement = select(Internship)

    if status_filter and status_filter.lower() != "all":
        statement = statement.where(Internship.status.ilike(status_filter))

    results = session.exec(statement).all()

    # Apply search filter
    if search and search.strip():
        q = search.strip().lower()
        results = [
            item for item in results
            if q in item.title.lower()
            or q in item.company_name.lower()
            or q in item.location.lower()
            or q in item.description.lower()
        ]

    # Return newest first
    return sorted(results, key=lambda x: x.created_at, reverse=True)


# =====================================================================
# DASHBOARD STATS SUMMARY
# =====================================================================

@router.get(
    "/internships/stats/summary",
    response_model=InternshipStats,
    tags=["Internships"],
    summary="Get aggregated statistics for the dashboard",
)
def get_stats(session: Session = Depends(get_session)):
    """Computes total, open, closed, and remote counts."""
    all_items = session.exec(select(Internship)).all()
    total = len(all_items)
    open_count = sum(1 for i in all_items if i.status.lower() == "open")
    closed_count = sum(1 for i in all_items if i.status.lower() == "closed")
    remote_count = sum(1 for i in all_items if "remote" in i.location.lower())

    return InternshipStats(
        total=total,
        open=open_count,
        closed=closed_count,
        remote=remote_count
    )


# =====================================================================
# 3. READ SINGLE OPERATION (R in CRUD - One Record)
# =====================================================================

@router.get(
    "/internships/{internship_id}",
    response_model=Internship,
    status_code=status.HTTP_200_OK,
    tags=["Internships"],
    summary="Get details of a specific internship by ID",
)
def get_internship_by_id(
    internship_id: str,
    session: Session = Depends(get_session)
):
    """
    Fetches a single internship opportunity by its unique UUID.
    - If found, returns HTTP 200 with the full internship details.
    - If not found in DB, checks seed records or raises HTTP 404.
    """
    internship = session.get(Internship, internship_id)
    if not internship:
        for item in SAMPLE_INTERNSHIPS:
            if item.get("id") == internship_id:
                internship = Internship(**item)
                session.add(internship)
                session.commit()
                session.refresh(internship)
                return internship
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Internship opportunity with ID '{internship_id}' was not found."
        )
    return internship


# =====================================================================
# 4. UPDATE OPERATION (U in CRUD)
# =====================================================================

@router.put(
    "/internships/{internship_id}",
    response_model=Internship,
    status_code=status.HTTP_200_OK,
    tags=["Internships"],
    summary="Update an existing internship opportunity",
)
def update_internship(
    internship_id: str,
    data: InternshipUpdate,
    session: Session = Depends(get_session)
):
    """
    Updates an existing internship record.
    - If found, updates only fields provided in the request body.
    - If not yet in the current container database, creates/upserts it seamlessly.
    - Commits changes to the database and returns updated object.
    """
    internship = session.get(Internship, internship_id)
    if not internship:
        # Check if ID is one of sample seeds to base initial data on
        base_data = {
            "title": "Internship Opportunity",
            "company_name": "Company",
            "location": "Remote",
            "description": "Role description",
            "salary": "Unpaid",
            "deadline": "2026-12-31",
            "status": "Open",
        }
        for item in SAMPLE_INTERNSHIPS:
            if item.get("id") == internship_id:
                base_data = dict(item)
                break
        base_data.update(data.model_dump(exclude_unset=True))
        base_data["id"] = internship_id
        internship = Internship(**base_data)
        session.add(internship)
        session.commit()
        session.refresh(internship)
        return internship

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(internship, key, value)

    session.add(internship)
    session.commit()
    session.refresh(internship)
    return internship


# =====================================================================
# 5. DELETE OPERATION (D in CRUD)
# =====================================================================

@router.delete(
    "/internships/{internship_id}",
    status_code=status.HTTP_200_OK,
    tags=["Internships"],
    summary="Delete an internship opportunity",
)
def delete_internship(
    internship_id: str,
    session: Session = Depends(get_session)
):
    """
    Deletes an internship record from the database.
    - Idempotent: If found, deletes record and commits transaction.
    - If not found or already deleted across serverless instances, returns HTTP 200 confirmation.
    """
    internship = session.get(Internship, internship_id)
    if internship:
        session.delete(internship)
        session.commit()

    return {
        "message": "Internship opportunity deleted successfully.",
        "id": internship_id
    }


# =====================================================================
# DEMO UTILITY: SEED RESET
# =====================================================================

@router.post(
    "/internships/seed/reset",
    status_code=status.HTTP_200_OK,
    tags=["Demo Utilities"],
    summary="Reset and re-populate the sample demo internships",
)
def reset_seed_data(session: Session = Depends(get_session)):
    """Deletes all existing internships and re-inserts the 5 sample demo records."""
    all_items = session.exec(select(Internship)).all()
    for item in all_items:
        session.delete(item)
    session.commit()

    for item in SAMPLE_INTERNSHIPS:
        session.add(Internship(**item))
    session.commit()

    return {"message": "Database reset and seeded successfully with 5 sample internships."}


# Mount the router under BOTH "/api" AND root "" so requests succeed regardless of Vercel rewrite handling
app.include_router(router, prefix="/api")
app.include_router(router, prefix="")


# =====================================================================
# FRONTEND STATIC FILES (Production / Vercel Serving)
# =====================================================================

FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"

if FRONTEND_DIST_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST_DIR), html=True), name="frontend")
