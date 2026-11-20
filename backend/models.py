"""
Data models and schemas for Internship Opportunity Manager.
Uses SQLModel (combining SQLAlchemy + Pydantic) for database tables and API validation.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


# ============================================================================
# User & Authentication Models (CSE309 Final Project)
# ============================================================================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    name: str = Field(description="Full name of the user")
    email: str = Field(unique=True, index=True, description="Unique email address")
    role: str = Field(default=UserRole.USER.value, description="User role: user or admin")
    is_banned: bool = Field(default=False, description="Flag indicating if account is banned")


class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique UUID identifier"
    )
    hashed_password: str = Field(description="Bcrypt hashed password")
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when created"
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when last updated"
    )


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique UUID identifier"
    )
    user_id: str = Field(index=True, foreign_key="users.id", description="Associated user ID")
    token_hash: str = Field(index=True, unique=True, description="Hashed or unique token string")
    expires_at: str = Field(description="Expiration timestamp string")
    is_revoked: bool = Field(default=False, description="Whether token was revoked by logout")
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when issued"
    )


class UserCreate(SQLModel):
    name: str
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: str
    name: str
    email: str
    role: str
    is_banned: bool
    created_at: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead


class TokenRefreshRequest(SQLModel):
    refresh_token: str


# ============================================================================
# Internship Models
# ============================================================================

class InternshipBase(SQLModel):
    title: str = Field(index=True, description="Job/Internship Title")
    company_name: str = Field(index=True, description="Company or Organization Name")
    location: str = Field(description="Location e.g. Dhaka, Remote, Hybrid")
    description: str = Field(description="Role description, responsibilities, and requirements")
    salary: str = Field(default="Unpaid", description="Salary or stipend e.g. ৳12,000/month, Unpaid")
    deadline: str = Field(description="Application deadline in YYYY-MM-DD format")
    status: str = Field(default="Open", description="Status: Open or Closed")


class Internship(InternshipBase, table=True):
    __tablename__ = "internships"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique UUID identifier"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when created"
    )


class InternshipCreate(InternshipBase):
    pass


class InternshipUpdate(SQLModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None


class InternshipStats(SQLModel):
    total: int
    open: int
    closed: int
    remote: int
