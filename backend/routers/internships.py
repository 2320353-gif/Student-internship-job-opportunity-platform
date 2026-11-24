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
        User,
    )
    from auth.dependencies import get_current_user_optional
except ImportError:
    from backend import crud
    from backend.database import get_session
    from backend.models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
        User,
    )
    from backend.auth.dependencies import get_current_user_optional

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
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: Session = Depends(get_session),
):
    """Creates a new internship record and binds to authenticated creator."""
    user_id = current_user.id if current_user else None
    return crud.create_internship(session=session, data=data, user_id=user_id)


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
    my_only: bool = Query(False, description="Filter only current user's postings"),
    group_id: Optional[str] = Query(None, description="Filter by group ID"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: Session = Depends(get_session),
):
    """Retrieves all internship opportunities via the CRUD service layer."""
    filter_user_id = current_user.id if (my_only and current_user) else None
    return crud.get_internships(
        session=session,
        search=search,
        status_filter=status_filter,
        user_id=filter_user_id,
        group_id=group_id,
    )


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
# 4. UPDATE OPERATION (U in CRUD) - RBAC & Ownership Enforced
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
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: Session = Depends(get_session),
):
    """Updates an existing internship record with strict RBAC ownership check."""
    internship = crud.get_internship_by_id(session=session, internship_id=internship_id)
    if not internship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Internship opportunity with ID '{internship_id}' was not found.",
        )

    # RBAC: Main Admin can update any; Security Officer can update student posts but NOT Main Admin posts; normal users can only update their own
    if current_user:
        is_owner = internship.user_id and internship.user_id == current_user.id
        is_main_admin = bool(getattr(current_user, "is_main_admin", False) or current_user.email == "admin@platform.com")
        is_admin_or_officer = current_user.role in ["admin", "security_officer"] or is_main_admin

        if internship.user_id and not is_owner:
            owner_user = session.get(User, internship.user_id)
            is_post_by_main_admin = owner_user and (getattr(owner_user, "is_main_admin", False) or owner_user.email == "admin@platform.com")
            if is_post_by_main_admin and not is_main_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: Security Officer cannot modify opportunities posted by the Admin Manager.",
                )

        if not is_admin_or_officer and not is_owner and internship.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only modify your own internship postings.",
            )

    return crud.update_internship(session=session, internship_id=internship_id, data=data)


# =====================================================================
# 5. DELETE OPERATION (D in CRUD) - RBAC & Ownership Enforced
# =====================================================================

@router.delete(
    "/internships/{internship_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an internship opportunity",
)
def delete_internship(
    internship_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    session: Session = Depends(get_session),
):
    """Deletes an internship record with strict RBAC ownership check and audit log."""
    internship = crud.get_internship_by_id(session=session, internship_id=internship_id)
    if not internship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Internship opportunity with ID '{internship_id}' was not found.",
        )

    # RBAC: Main Admin can delete any; Security Officer can delete student posts but NOT Main Admin posts; normal users can only delete their own
    if current_user:
        is_owner = internship.user_id and internship.user_id == current_user.id
        is_main_admin = bool(getattr(current_user, "is_main_admin", False) or current_user.email == "admin@platform.com")
        is_admin_or_officer = current_user.role in ["admin", "security_officer"] or is_main_admin

        if internship.user_id and not is_owner:
            owner_user = session.get(User, internship.user_id)
            is_post_by_main_admin = owner_user and (getattr(owner_user, "is_main_admin", False) or owner_user.email == "admin@platform.com")
            if is_post_by_main_admin and not is_main_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: Security Officer cannot delete opportunities posted by the Admin Manager.",
                )

        if not is_admin_or_officer and not is_owner and internship.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only delete your own internship postings.",
            )

    # Record audit log
    crud.record_audit_event(
        session=session,
        action="DELETE_OPPORTUNITY",
        details=f"Opportunity '{internship.title}' at '{internship.company_name}' deleted.",
        user_id=current_user.id if current_user else None,
        user_email=current_user.email if current_user else None,
    )

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
