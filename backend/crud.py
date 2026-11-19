"""
CRUD and Database Operations for Internship Opportunity Manager.
Encapsulates all database interactions and business logic outside route handlers.
Follows CSE309 repository / service / crud pattern.
"""

import sys
from pathlib import Path
from typing import List, Optional

# Ensure paths are set
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from sqlmodel import Session, select

try:
    from database import SAMPLE_INTERNSHIPS
    from models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )
except ImportError:
    from backend.database import SAMPLE_INTERNSHIPS
    from backend.models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )


# =====================================================================
# 1. CREATE (C in CRUD)
# =====================================================================

def create_internship(session: Session, data: InternshipCreate) -> Internship:
    """
    Creates a new internship record.
    - Validates payload using SQLModel
    - Persists record to the database
    - Returns the newly created internship
    """
    internship = Internship.model_validate(data)
    session.add(internship)
    session.commit()
    session.refresh(internship)
    return internship


# =====================================================================
# 2. READ LIST (R in CRUD - All Records)
# =====================================================================

def get_internships(
    session: Session,
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
) -> List[Internship]:
    """
    Retrieves all internship opportunities from the database.
    - Supports optional keyword search in title, company_name, location, description
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
# 3. READ SINGLE (R in CRUD - One Record)
# =====================================================================

def get_internship_by_id(session: Session, internship_id: str) -> Optional[Internship]:
    """
    Fetches a single internship opportunity by its unique UUID.
    - If found, returns the internship.
    - If not in DB, checks sample seed data for serverless resilience.
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
        return None
    return internship


# =====================================================================
# 4. UPDATE (U in CRUD)
# =====================================================================

def update_internship(
    session: Session,
    internship_id: str,
    data: InternshipUpdate,
) -> Internship:
    """
    Updates an existing internship record.
    - If found, updates only fields provided in the request body.
    - If not yet in the current container database, upserts it seamlessly.
    - Commits changes to the database and returns updated object.
    """
    internship = session.get(Internship, internship_id)
    if not internship:
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
# 5. DELETE (D in CRUD)
# =====================================================================

def delete_internship(session: Session, internship_id: str) -> bool:
    """
    Deletes an internship record from the database.
    - Idempotent: If found, deletes record and commits transaction.
    - Returns True if deleted or already absent.
    """
    internship = session.get(Internship, internship_id)
    if internship:
        session.delete(internship)
        session.commit()
    return True


# =====================================================================
# DASHBOARD STATS SUMMARY
# =====================================================================

def get_stats(session: Session) -> InternshipStats:
    """Computes aggregated statistics: total, open, closed, and remote counts."""
    all_items = session.exec(select(Internship)).all()
    total = len(all_items)
    open_count = sum(1 for i in all_items if i.status.lower() == "open")
    closed_count = sum(1 for i in all_items if i.status.lower() == "closed")
    remote_count = sum(1 for i in all_items if "remote" in i.location.lower())

    return InternshipStats(
        total=total,
        open=open_count,
        closed=closed_count,
        remote=remote_count,
    )


# =====================================================================
# DEMO UTILITY: SEED RESET
# =====================================================================

def reset_seed_data(session: Session) -> None:
    """Deletes all existing internships and re-inserts the 5 sample demo records."""
    all_items = session.exec(select(Internship)).all()
    for item in all_items:
        session.delete(item)
    session.commit()

    for item in SAMPLE_INTERNSHIPS:
        session.add(Internship(**item))
    session.commit()
