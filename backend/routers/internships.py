"""
Router module for Internship Opportunity endpoints.
Delegates all database queries and business logic to crud / service layer.
Follows separation of concerns (CSE309 MVP requirement).
"""

import sys
from pathlib import Path
from typing import List, Optional

# Ensure paths are set
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

try:
    import crud
    from database import get_session
    from models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )
except ImportError:
    from backend import crud
    from backend.database import get_session
    from backend.models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )

router = APIRouter(tags=["Internships"])


# =====================================================================
# 1. CREATE OPERATION (C in CRUD)
# =====================================================================

@router.post(
    "/internships",
    response_model=Internship,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new internship opportunity",
)
def create_internship(
    data: InternshipCreate,
    session: Session = Depends(get_session),
):
    """Creates a new internship record via the CRUD service layer."""
    return crud.create_internship(session=session, data=data)


# =====================================================================
# 2. READ LIST OPERATION (R in CRUD - All Records)
# =====================================================================

@router.get(
    "/internships",
    response_model=List[Internship],
    status_code=status.HTTP_200_OK,
    summary="Get all internships with optional search and filter",
)
def get_internships(
    search: Optional[str] = Query(None, description="Search by title, company, or location"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: Open or Closed"),
    session: Session = Depends(get_session),
):
    """Retrieves all internship opportunities via the CRUD service layer."""
    return crud.get_internships(session=session, search=search, status_filter=status_filter)


# =====================================================================
# DASHBOARD STATS SUMMARY
# =====================================================================

@router.get(
    "/internships/stats/summary",
    response_model=InternshipStats,
    summary="Get aggregated statistics for the dashboard",
)
def get_stats(session: Session = Depends(get_session)):
    """Computes aggregated dashboard statistics via the CRUD service layer."""
    return crud.get_stats(session=session)


# =====================================================================
# 3. READ SINGLE OPERATION (R in CRUD - One Record)
# =====================================================================

@router.get(
    "/internships/{internship_id}",
    response_model=Internship,
    status_code=status.HTTP_200_OK,
    summary="Get details of a specific internship by ID",
)
def get_internship_by_id(
    internship_id: str,
    session: Session = Depends(get_session),
):
    """Fetches a single internship opportunity by its unique UUID."""
    internship = crud.get_internship_by_id(session=session, internship_id=internship_id)
    if not internship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Internship opportunity with ID '{internship_id}' was not found.",
        )
    return internship


# =====================================================================
# 4. UPDATE OPERATION (U in CRUD)
# =====================================================================

@router.put(
    "/internships/{internship_id}",
    response_model=Internship,
    status_code=status.HTTP_200_OK,
    summary="Update an existing internship opportunity",
)
def update_internship(
    internship_id: str,
    data: InternshipUpdate,
    session: Session = Depends(get_session),
):
    """Updates an existing internship record via the CRUD service layer."""
    return crud.update_internship(session=session, internship_id=internship_id, data=data)


# =====================================================================
# 5. DELETE OPERATION (D in CRUD)
# =====================================================================

@router.delete(
    "/internships/{internship_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an internship opportunity",
)
def delete_internship(
    internship_id: str,
    session: Session = Depends(get_session),
):
    """Deletes an internship record via the CRUD service layer."""
    crud.delete_internship(session=session, internship_id=internship_id)
    return {
        "message": "Internship opportunity deleted successfully.",
        "id": internship_id,
    }


# =====================================================================
# DEMO UTILITY: SEED RESET
# =====================================================================

@router.post(
    "/internships/seed/reset",
    status_code=status.HTTP_200_OK,
    summary="Reset and re-populate the sample demo internships",
)
def reset_seed_data(session: Session = Depends(get_session)):
    """Resets database seed records via the CRUD service layer."""
    crud.reset_seed_data(session=session)
    return {"message": "Database reset and seeded successfully with 5 sample internships."}
