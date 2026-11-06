"""
Database configuration and session management for Internship Opportunity Manager.
Supports local SQLite database by default, and Supabase / PostgreSQL via DATABASE_URL.
Engineered for reliable execution across local, Docker, and Vercel Serverless environments.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

# Ensure backend directory and project root are in sys.path
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from models import Internship
except ImportError:
    from backend.models import Internship


def init_engine():
    """
    Initializes a resilient database engine.
    1. Checks external DATABASE_URL (e.g. Supabase Postgres)
    2. Checks SQLite candidate file locations (temp directory or local)
    3. Seamlessly falls back to StaticPool SQLite in-memory if disk access is restricted
    """
    # 1. External DATABASE_URL (Supabase/PostgreSQL) if configured
    env_db_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DATABASE_URL")
    if env_db_url:
        if env_db_url.startswith("postgres://"):
            env_db_url = env_db_url.replace("postgres://", "postgresql://", 1)
        try:
            eng = create_engine(env_db_url, echo=False)
            with eng.connect():
                pass
            return eng
        except Exception as e:
            print(f"DATABASE_URL connect failed: {e}")

    # 2. SQLite candidates
    temp_dir = Path(tempfile.gettempdir())
    candidates = []

    # On Vercel / AWS Lambda serverless, prioritize /tmp and system temp directory
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME") or os.getenv("VERCEL_ENV"):
        candidates.append(temp_dir / "internships.db")
        candidates.append(Path("/tmp/internships.db"))
    else:
        candidates.append(BASE_DIR / "internships.db")
        candidates.append(temp_dir / "internships.db")

    for db_path in candidates:
        try:
            db_path.parent.mkdir(parents=True, exist_ok=True)
            norm = str(db_path.resolve()).replace("\\", "/")
            url = f"sqlite:///{norm}" if not norm.startswith("/") else f"sqlite://{norm}"
            eng = create_engine(url, echo=False, connect_args={"check_same_thread": False})
            with eng.connect():
                pass
            return eng
        except Exception as e:
            print(f"SQLite file engine failed for {db_path}: {e}")

    # 3. Guaranteed in-memory fallback with StaticPool so state persists across connections
    return create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )


engine = init_engine()


# Deterministic UUIDs matching frontend seeds for serverless consistency across lambda instances
SAMPLE_INTERNSHIPS = [
    {
        "id": "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f60",
        "title": "Frontend Developer Intern",
        "company_name": "ABC Technologies",
        "location": "Dhaka, Bangladesh",
        "description": "Join our dynamic frontend engineering squad. Work with React, TypeScript, and modern CSS frameworks to build responsive, accessible web portals.",
        "salary": "৳12,000 / month",
        "deadline": "2026-11-28",
        "status": "Open",
    },
    {
        "id": "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f61",
        "title": "Python & FastAPI Backend Intern",
        "company_name": "XYZ Software Solutions",
        "location": "Remote",
        "description": "Assist in building high-performance asynchronous RESTful APIs with FastAPI, SQLModel, and PostgreSQL. Great learning opportunity with senior mentorship.",
        "salary": "৳15,000 / month",
        "deadline": "2026-11-30",
        "status": "Open",
    },
    {
        "id": "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f62",
        "title": "UI/UX Designer Intern",
        "company_name": "Creative Studio Lab",
        "location": "Dhaka, Bangladesh",
        "description": "Design wireframes, high-fidelity prototypes in Figma, and conduct usability tests for student productivity apps and job boards.",
        "salary": "৳10,000 / month",
        "deadline": "2026-11-15",
        "status": "Closed",
    },
    {
        "id": "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f63",
        "title": "Data Science & Analytics Intern",
        "company_name": "FinTech Matrix",
        "location": "Hybrid (Dhaka)",
        "description": "Clean, process, and analyze financial data using Pandas and SQL. Build exploratory visualization dashboards for executive decision making.",
        "salary": "৳14,000 / month",
        "deadline": "2026-12-05",
        "status": "Open",
    },
    {
        "id": "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f64",
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
    try:
        existing = session.exec(select(Internship)).first()
        if not existing:
            for item in SAMPLE_INTERNSHIPS:
                internship = Internship(**item)
                session.add(internship)
            session.commit()
    except Exception as e:
        print(f"Seed data notice: {e}")


def init_db() -> None:
    """Create all tables and seed initial records on application startup."""
    try:
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            seed_data(session)
    except Exception as e:
        print(f"Database init notice: {e}")


# Initialize tables and seed records immediately
init_db()


def get_session() -> Generator[Session, None, None]:
    """Dependency injection for FastAPI endpoints to get a DB session."""
    with Session(engine) as session:
        yield session
