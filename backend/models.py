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
    SECURITY_OFFICER = "security_officer"


class UserBase(SQLModel):
    name: str = Field(description="Full name of the user")
    email: str = Field(unique=True, index=True, description="Unique email address")
    role: str = Field(default=UserRole.USER.value, description="User role: user, admin, or security_officer")
    is_main_admin: bool = Field(default=False, description="Whether this user is the root Main Admin (Admin Manager)")
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
    is_main_admin: bool = False
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
# Internship Models (With Ownership and Group Association)
# ============================================================================

class InternshipBase(SQLModel):
    title: str = Field(index=True, description="Job/Internship Title")
    company_name: str = Field(index=True, description="Company or Organization Name")
    location: str = Field(description="Location e.g. Dhaka, Remote, Hybrid")
    description: str = Field(description="Role description, responsibilities, and requirements")
    salary: str = Field(default="Unpaid", description="Salary or stipend e.g. ৳12,000/month, Unpaid")
    deadline: str = Field(description="Application deadline in YYYY-MM-DD format")
    status: str = Field(default="Open", description="Status: Open or Closed")
    user_id: Optional[str] = Field(default=None, foreign_key="users.id", index=True, description="Owner user ID")
    group_id: Optional[str] = Field(default=None, foreign_key="groups.id", index=True, description="Optional team group ID")


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


class InternshipCreate(SQLModel):
    title: str
    company_name: str
    location: str
    description: str
    salary: str = "Unpaid"
    deadline: str
    status: str = "Open"
    group_id: Optional[str] = None


class InternshipUpdate(SQLModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None
    group_id: Optional[str] = None


class InternshipStats(SQLModel):
    total: int
    open: int
    closed: int
    remote: int


# ============================================================================
# Shared Groups & Collaboration Models (Part 4)
# ============================================================================

class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique UUID identifier"
    )
    name: str = Field(index=True, description="Group / Career Club Name")
    description: str = Field(default="", description="Group focus and goals")
    owner_id: str = Field(foreign_key="users.id", index=True, description="Creator and Owner user ID")
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when created"
    )


class GroupMember(SQLModel, table=True):
    __tablename__ = "group_members"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique UUID identifier"
    )
    group_id: str = Field(foreign_key="groups.id", index=True, description="Associated group ID")
    user_id: str = Field(foreign_key="users.id", index=True, description="Associated user ID")
    can_create: bool = Field(default=True, description="Permission to post opportunities under group")
    can_edit: bool = Field(default=False, description="Permission to edit group opportunities")
    can_assign: bool = Field(default=False, description="Permission to assign opportunities to members")
    joined_at: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp when joined"
    )


class GroupCreate(SQLModel):
    name: str
    description: str = ""


class GroupMemberAdd(SQLModel):
    email: str
    can_create: bool = True
    can_edit: bool = False
    can_assign: bool = False


class GroupMemberRead(SQLModel):
    id: str
    user_id: str
    name: str
    email: str
    can_create: bool
    can_edit: bool
    can_assign: bool
    is_owner: bool
    joined_at: str


class GroupRead(SQLModel):
    id: str
    name: str
    description: str
    owner_id: str
    owner_name: Optional[str] = None
    created_at: str
    members_count: int = 0
    members: list[GroupMemberRead] = []


# ============================================================================
# Audit Logs & Admin Overview Models (Part 5)
# ============================================================================

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique UUID identifier"
    )
    user_id: Optional[str] = Field(default=None, index=True, description="Acting user ID if known")
    user_email: Optional[str] = Field(default=None, description="Acting user email")
    action: str = Field(index=True, description="Action code e.g. LOGIN_SUCCESS, BAN_USER, DELETE_OPP")
    details: str = Field(default="", description="Detailed human-readable log message")
    ip_address: str = Field(default="127.0.0.1", description="Client IP address")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        description="Event timestamp"
    )


class AuditLogRead(SQLModel):
    id: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    action: str
    details: str
    ip_address: str
    timestamp: str


class AdminOverviewStats(SQLModel):
    total_users: int
    banned_users: int
    admin_users: int
    total_opportunities: int
    open_opportunities: int
    total_groups: int
    total_audit_logs: int

