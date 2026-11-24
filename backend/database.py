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
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

# Ensure backend directory and project root are in sys.path
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from models import Internship, User, RefreshToken, Group, GroupMember, AuditLog
except ImportError:
    from backend.models import Internship, User, RefreshToken, Group, GroupMember, AuditLog
import bcrypt


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
    """Populates sample internships, teacher demo accounts, and shared group if database is empty."""
    try:
        demo_password_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt(12)).decode("utf-8")

        # 1. Five Teacher-Mandated Demo Accounts
        accounts = [
            ("a1000000-0000-0000-0000-000000000001", "Admin Manager", "admin@platform.com", "admin", True),
            ("a1000000-0000-0000-0000-000000000002", "Security Officer", "admin2@platform.com", "admin", False),
            ("b2000000-0000-0000-0000-000000000001", "Afrin Sultana", "student@university.edu", "user", False),
            ("b2000000-0000-0000-0000-000000000002", "Rahim Ahmed", "student2@university.edu", "user", False),
            ("b2000000-0000-0000-0000-000000000003", "Karim Hasan", "student3@university.edu", "user", False),
        ]

        for user_id, name, email, role, is_main in accounts:
            user = session.exec(select(User).where(User.email == email)).first()
            if not user:
                user = User(
                    id=user_id,
                    name=name,
                    email=email,
                    hashed_password=demo_password_hash,
                    role=role,
                    is_main_admin=is_main,
                    is_banned=False,
                )
                session.add(user)
            else:
                # Update existing records to reflect main admin status and accurate names
                user.name = name
                user.is_main_admin = is_main
                session.add(user)

        session.commit()

        # 2. Seed 1 Shared Group with Mixed Member Permissions (Teacher Requirement)
        group_id = "c3000000-0000-0000-0000-000000000001"
        group = session.exec(select(Group).where(Group.id == group_id)).first()
        if not group:
            group = Group(
                id=group_id,
                name="Career Builders Club",
                description="Collaborative student initiative for tech internships and engineering jobs",
                owner_id="b2000000-0000-0000-0000-000000000001",  # Owned by Afrin
            )
            session.add(group)
            session.commit()

            # Member 1: Afrin (Owner - full permissions)
            session.add(GroupMember(
                group_id=group_id,
                user_id="b2000000-0000-0000-0000-000000000001",
                can_create=True,
                can_edit=True,
                can_assign=True
            ))
            # Member 2: Rahim (Editor & Assigner)
            session.add(GroupMember(
                group_id=group_id,
                user_id="b2000000-0000-0000-0000-000000000002",
                can_create=True,
                can_edit=True,
                can_assign=True
            ))
            # Member 3: Karim (Poster only)
            session.add(GroupMember(
                group_id=group_id,
                user_id="b2000000-0000-0000-0000-000000000003",
                can_create=True,
                can_edit=False,
                can_assign=False
            ))
            session.commit()

        # 3. Seed Sample Internships with User Ownership
        existing = session.exec(select(Internship)).first()
        if not existing:
            for item in SAMPLE_INTERNSHIPS:
                internship_data = item.copy()
                internship_data["user_id"] = "b2000000-0000-0000-0000-000000000001"  # Owned by Afrin
                internship_data["group_id"] = group_id
                internship = Internship(**internship_data)
                session.add(internship)
            session.commit()

        # 4. Initial Audit Log
        existing_log = session.exec(select(AuditLog)).first()
        if not existing_log:
            session.add(AuditLog(
                action="SYSTEM_INIT",
                details="Platform database initialized with 5 demo accounts and 1 shared group.",
                user_email="system@opportunityhub.internal",
                ip_address="127.0.0.1"
            ))
            session.commit()

    except Exception as e:
        print(f"Seed data notice: {e}")


def auto_migrate(eng) -> None:
    """Safely adds missing columns to existing SQLite tables if schema was updated."""
    try:
        with eng.connect() as conn:
            # Check columns in internships
            res = conn.execute(text("PRAGMA table_info(internships);")).fetchall()
            cols = [r[1] for r in res] if res else []
            if cols:
                if "user_id" not in cols:
                    conn.execute(text("ALTER TABLE internships ADD COLUMN user_id VARCHAR;"))
                if "group_id" not in cols:
                    conn.execute(text("ALTER TABLE internships ADD COLUMN group_id VARCHAR;"))
                conn.commit()

            # Check columns in users
            user_res = conn.execute(text("PRAGMA table_info(users);")).fetchall()
            user_cols = [r[1] for r in user_res] if user_res else []
            if user_cols:
                if "is_main_admin" not in user_cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_main_admin BOOLEAN DEFAULT 0;"))
                conn.commit()
    except Exception as e:
        print(f"Migration notice: {e}")


def init_db() -> None:
    """Create all tables and seed initial records on application startup."""
    try:
        auto_migrate(engine)
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
