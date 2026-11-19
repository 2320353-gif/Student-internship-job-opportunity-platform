"""
Service layer for Internship operations.
Coordinates business logic and CRUD operations.
"""

from typing import List, Optional
from sqlmodel import Session

try:
    import crud
    from models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )
except ImportError:
    from backend import crud
    from backend.models import (
        Internship,
        InternshipCreate,
        InternshipStats,
        InternshipUpdate,
    )


class InternshipService:
    @staticmethod
    def list_internships(
        session: Session,
        search: Optional[str] = None,
        status_filter: Optional[str] = None,
    ) -> List[Internship]:
        return crud.get_internships(session=session, search=search, status_filter=status_filter)

    @staticmethod
    def get_by_id(session: Session, internship_id: str) -> Optional[Internship]:
        return crud.get_internship_by_id(session=session, internship_id=internship_id)

    @staticmethod
    def create(session: Session, data: InternshipCreate) -> Internship:
        return crud.create_internship(session=session, data=data)

    @staticmethod
    def update(session: Session, internship_id: str, data: InternshipUpdate) -> Internship:
        return crud.update_internship(session=session, internship_id=internship_id, data=data)

    @staticmethod
    def delete(session: Session, internship_id: str) -> bool:
        return crud.delete_internship(session=session, internship_id=internship_id)

    @staticmethod
    def get_dashboard_stats(session: Session) -> InternshipStats:
        return crud.get_stats(session=session)

    @staticmethod
    def reset_seed(session: Session) -> None:
        crud.reset_seed_data(session=session)
