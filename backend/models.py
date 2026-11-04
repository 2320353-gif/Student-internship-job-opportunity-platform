"""
Data models and schemas for Internship Opportunity Manager.
Uses SQLModel (combining SQLAlchemy + Pydantic) for database tables and API validation.
"""

from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


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
