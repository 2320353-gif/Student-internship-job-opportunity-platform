"""
Database configuration and session management for Internship Opportunity Manager.
Supports local SQLite database by default, and Supabase / PostgreSQL via DATABASE_URL.
"""

import os
from pathlib import Path
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine, select
from models import Internship

# Database path configuration
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_FILE = BASE_DIR / "internships.db"
DEFAULT_SQLITE_URL = f"sqlite:///{DEFAULT_DB_FILE}"

# Read environment variables (e.g. Supabase PostgreSQL URL)
database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DATABASE_URL") or DEFAULT_SQLITE_URL

# Fix SQLAlchemy URL scheme if provided as "postgres://"
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# SQLite requires check_same_thread=False for FastAPI concurrency
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(database_url, echo=False, connect_args=connect_args)


def get_session() -> Generator[Session, None, None]:
    """Dependency injection for FastAPI endpoints to get a DB session."""
    with Session(engine) as session:
        yield session


SAMPLE_INTERNSHIPS = [
    {
        "title": "Frontend Developer Intern",
        "company_name": "ABC Technologies",
        "location": "Dhaka, Bangladesh",
        "description": "Join our dynamic frontend engineering squad. Work with React, TypeScript, and modern CSS frameworks to build responsive, accessible web portals.",
        "salary": "৳12,000 / month",
        "deadline": "2026-11-28",
        "status": "Open",
    },
    {
        "title": "Python & FastAPI Backend Intern",
        "company_name": "XYZ Software Solutions",
        "location": "Remote",
        "description": "Assist in building high-performance asynchronous RESTful APIs with FastAPI, SQLModel, and PostgreSQL. Great learning opportunity with senior mentorship.",
        "salary": "৳15,000 / month",
        "deadline": "2026-11-30",
        "status": "Open",
    },
    {
        "title": "UI/UX Designer Intern",
        "company_name": "Creative Studio Lab",
        "location": "Dhaka, Bangladesh",
        "description": "Design wireframes, high-fidelity prototypes in Figma, and conduct usability tests for student productivity apps and job boards.",
        "salary": "৳10,000 / month",
        "deadline": "2026-11-15",
        "status": "Closed",
    },
    {
        "title": "Data Science & Analytics Intern",
        "company_name": "FinTech Matrix",
        "location": "Hybrid (Dhaka)",
        "description": "Clean, process, and analyze financial data using Pandas and SQL. Build exploratory visualization dashboards for executive decision making.",
        "salary": "৳14,000 / month",
        "deadline": "2026-12-05",
        "status": "Open",
    },
    {
        "title": "Full Stack Engineering Intern",
        "company_name": "CloudCraft Systems",
        "location": "Remote",
        "description": "Hands-on experience developing end-to-end web features connecting React frontends with Python microservices and Supabase cloud databases.",
        "salary": "৳18,000 / month",
        "deadline": "2026-12-15",
        "status": "Open",
    },
]


def seed_data(session: Session) -> None:
    """Populates sample internships if the database table is empty."""
    existing = session.exec(select(Internship)).first()
    if not existing:
        for item in SAMPLE_INTERNSHIPS:
            internship = Internship(**item)
            session.add(internship)
        session.commit()
        print("Initialized database with realistic seed internships.")


def init_db() -> None:
    """Create all tables and seed initial records on application startup."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_data(session)
