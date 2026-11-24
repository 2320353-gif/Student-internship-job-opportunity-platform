"""
Admin router: Command center metrics, user management, account banning, audit logs, and CSV export.
Requires 'admin' role privileges (CSE309 Final Project Part 5).
"""

import csv
import io
import sys
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, select

try:
    import crud
    from database import get_session
    from models import (
        AdminOverviewStats,
        AuditLog,
        AuditLogRead,
        Group,
        Internship,
        RefreshToken,
        User,
        UserRead,
    )
    from auth.dependencies import require_admin
except ImportError:
    from backend import crud
    from backend.database import get_session
    from backend.models import (
        AdminOverviewStats,
        AuditLog,
        AuditLogRead,
        Group,
        Internship,
        RefreshToken,
        User,
        UserRead,
    )
    from backend.auth.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin Command Center"])


@router.get("/overview", response_model=AdminOverviewStats)
def get_admin_overview(
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Computes high-level platform statistics for the administrator dashboard."""
    users = session.exec(select(User)).all()
    banned_users = len([u for u in users if u.is_banned])
    admin_users = len([u for u in users if u.role == "admin"])

    internships = session.exec(select(Internship)).all()
    open_opps = len([i for i in internships if i.status.lower() == "open"])

    groups = session.exec(select(Group)).all()
    audit_logs = session.exec(select(AuditLog)).all()

    return AdminOverviewStats(
        total_users=len(users),
        banned_users=banned_users,
        admin_users=admin_users,
        total_opportunities=len(internships),
        open_opportunities=open_opps,
        total_groups=len(groups),
        total_audit_logs=len(audit_logs),
    )


@router.get("/users", response_model=List[UserRead])
def list_all_users(
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[str] = Query(None, description="Filter by role: user or admin"),
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Retrieves all registered users with optional search and role filtering."""
    statement = select(User)
    if role:
        statement = statement.where(User.role == role)

    users = session.exec(statement).all()
    if search and search.strip():
        q = search.strip().lower()
        users = [u for u in users if q in u.name.lower() or q in u.email.lower()]

    return sorted(users, key=lambda u: u.created_at, reverse=True)


def is_main_admin_user(user: User) -> bool:
    """Returns True if the user is the root Main Admin (Admin Manager)."""
    return bool(getattr(user, "is_main_admin", False) or user.email == "admin@platform.com")


@router.post("/users/{user_id}/ban", response_model=UserRead)
def toggle_user_ban(
    user_id: str,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Bans or unbans a user account. Banned users are rejected with HTTP 403."""
    target_user = session.get(User, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if target_user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot ban your own administrator account."
        )

    # Security Officer & other admins CANNOT ban the Admin Manager
    if is_main_admin_user(target_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: The Main Admin (Admin Manager) is permanently protected and cannot be banned."
        )

    # Toggle ban status
    target_user.is_banned = not target_user.is_banned
    session.add(target_user)

    # If banning, revoke all active sessions immediately
    if target_user.is_banned:
        tokens = session.exec(
            select(RefreshToken).where(RefreshToken.user_id == target_user.id)
        ).all()
        for t in tokens:
            t.is_revoked = True
            session.add(t)

    session.commit()
    session.refresh(target_user)

    action_label = "BAN_USER" if target_user.is_banned else "UNBAN_USER"
    crud.record_audit_event(
        session=session,
        action=action_label,
        details=f"User {target_user.email} was {'banned' if target_user.is_banned else 'unbanned'} by Admin {admin.email}",
        user_id=admin.id,
        user_email=admin.email,
    )

    return target_user


@router.post("/users/{user_id}/role", response_model=UserRead)
def toggle_user_role(
    user_id: str,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Promotes a student to Admin or demotes an Admin to normal student."""
    target_user = session.get(User, user_id)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if target_user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own administrator role."
        )

    # Security Officer & other admins CANNOT change or demote Admin Manager
    if is_main_admin_user(target_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: The Main Admin (Admin Manager) role is permanently protected and cannot be modified."
        )

    new_role = "admin" if target_user.role == "user" else "user"
    target_user.role = new_role
    session.add(target_user)
    session.commit()
    session.refresh(target_user)

    crud.record_audit_event(
        session=session,
        action="CHANGE_ROLE",
        details=f"User {target_user.email} role updated to '{new_role}' by Admin {admin.email}",
        user_id=admin.id,
        user_email=admin.email,
    )

    return target_user


@router.get("/audit-logs", response_model=List[AuditLogRead])
def get_audit_trail(
    limit: int = Query(100, description="Max records to return"),
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Retrieves chronological audit log trail tracking platform events."""
    logs = session.exec(select(AuditLog)).all()
    logs_sorted = sorted(logs, key=lambda l: l.timestamp, reverse=True)[:limit]
    return logs_sorted


@router.get("/export/csv")
def export_csv(
    data_type: str = Query("opportunities", description="Data to export: 'opportunities' or 'users'"),
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Generates and downloads a CSV spreadsheet of opportunities or user accounts."""
    output = io.StringIO()
    writer = csv.writer(output)

    if data_type == "users":
        writer.writerow(["ID", "Name", "Email", "Role", "Is Banned", "Created At"])
        users = session.exec(select(User)).all()
        for u in users:
            writer.writerow([u.id, u.name, u.email, u.role, u.is_banned, u.created_at])
        filename = "opportunityhub_users.csv"
    else:
        writer.writerow(["ID", "Title", "Company", "Location", "Salary", "Deadline", "Status", "Owner ID", "Created At"])
        internships = session.exec(select(Internship)).all()
        for i in internships:
            writer.writerow([i.id, i.title, i.company_name, i.location, i.salary, i.deadline, i.status, i.user_id, i.created_at])
        filename = "opportunityhub_opportunities.csv"

    csv_content = output.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
