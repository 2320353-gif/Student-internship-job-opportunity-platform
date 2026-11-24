"""
Router module for Shared Groups & Teams Collaboration (CSE309 Final Project Part 4).
Enforces owner-only management and granular member permissions (create, edit, assign).
"""

import sys
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

try:
    import crud
    from database import get_session
    from models import (
        Group,
        GroupCreate,
        GroupMember,
        GroupMemberAdd,
        GroupMemberRead,
        GroupRead,
        User,
    )
    from auth.dependencies import get_current_active_user
except ImportError:
    from backend import crud
    from backend.database import get_session
    from backend.models import (
        Group,
        GroupCreate,
        GroupMember,
        GroupMemberAdd,
        GroupMemberRead,
        GroupRead,
        User,
    )
    from backend.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/groups", tags=["Groups & Collaboration"])


def get_group_or_404(group_id: str, session: Session) -> Group:
    group = session.get(Group, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with ID '{group_id}' was not found.",
        )
    return group


def check_group_owner(group: Group, current_user: User):
    """Enforces owner-only restriction for group management."""
    if current_user.role != "admin" and group.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Only the group owner can manage or delete this group.",
        )


@router.get("", response_model=List[GroupRead])
def list_groups(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Lists all groups the authenticated user belongs to (or all if admin)."""
    if current_user.role == "admin":
        groups = session.exec(select(Group)).all()
    else:
        # Find groups where user is owner or member
        member_records = session.exec(
            select(GroupMember).where(GroupMember.user_id == current_user.id)
        ).all()
        group_ids = {m.group_id for m in member_records}
        owned_groups = session.exec(
            select(Group).where(Group.owner_id == current_user.id)
        ).all()
        for og in owned_groups:
            group_ids.add(og.id)

        groups = session.exec(select(Group).where(Group.id.in_(list(group_ids)))).all() if group_ids else []

    output = []
    for g in groups:
        owner = session.get(User, g.owner_id)
        members = session.exec(select(GroupMember).where(GroupMember.group_id == g.id)).all()
        output.append(GroupRead(
            id=g.id,
            name=g.name,
            description=g.description,
            owner_id=g.owner_id,
            owner_name=owner.name if owner else "Unknown",
            created_at=g.created_at,
            members_count=len(members),
        ))
    return output


@router.post("", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(
    data: GroupCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Creates a new collaboration group. Creator automatically becomes Owner."""
    new_group = Group(
        name=data.name.strip(),
        description=data.description.strip(),
        owner_id=current_user.id,
    )
    session.add(new_group)
    session.commit()
    session.refresh(new_group)

    # Automatically add owner as first member with full permissions
    owner_member = GroupMember(
        group_id=new_group.id,
        user_id=current_user.id,
        can_create=True,
        can_edit=True,
        can_assign=True,
    )
    session.add(owner_member)
    session.commit()

    crud.record_audit_event(
        session=session,
        action="CREATE_GROUP",
        details=f"Group '{new_group.name}' created by {current_user.email}",
        user_id=current_user.id,
        user_email=current_user.email,
    )

    return GroupRead(
        id=new_group.id,
        name=new_group.name,
        description=new_group.description,
        owner_id=new_group.owner_id,
        owner_name=current_user.name,
        created_at=new_group.created_at,
        members_count=1,
    )


@router.get("/{group_id}", response_model=GroupRead)
def get_group_details(
    group_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Retrieves full group profile and roster of members with their permissions."""
    group = get_group_or_404(group_id, session)
    owner = session.get(User, group.owner_id)

    members_raw = session.exec(select(GroupMember).where(GroupMember.group_id == group.id)).all()
    members_list = []
    for m in members_raw:
        u = session.get(User, m.user_id)
        if u:
            members_list.append(GroupMemberRead(
                id=m.id,
                user_id=u.id,
                name=u.name,
                email=u.email,
                can_create=m.can_create,
                can_edit=m.can_edit,
                can_assign=m.can_assign,
                is_owner=(u.id == group.owner_id),
                joined_at=m.joined_at,
            ))

    return GroupRead(
        id=group.id,
        name=group.name,
        description=group.description,
        owner_id=group.owner_id,
        owner_name=owner.name if owner else "Unknown",
        created_at=group.created_at,
        members_count=len(members_list),
        members=members_list,
    )


@router.post("/{group_id}/members", response_model=GroupMemberRead, status_code=status.HTTP_201_CREATED)
def add_group_member(
    group_id: str,
    data: GroupMemberAdd,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Adds a new member to the group with granular permissions (Owner only)."""
    group = get_group_or_404(group_id, session)
    check_group_owner(group, current_user)

    target_email = data.email.strip().lower()
    target_user = session.exec(select(User).where(User.email == target_email)).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with email '{target_email}' found to invite.",
        )

    # Check if already a member
    existing = session.exec(
        select(GroupMember).where(
            GroupMember.group_id == group.id,
            GroupMember.user_id == target_user.id
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already a member of the group.",
        )

    member = GroupMember(
        group_id=group.id,
        user_id=target_user.id,
        can_create=data.can_create,
        can_edit=data.can_edit,
        can_assign=data.can_assign,
    )
    session.add(member)
    session.commit()
    session.refresh(member)

    crud.record_audit_event(
        session=session,
        action="ADD_GROUP_MEMBER",
        details=f"User {target_user.email} added to group '{group.name}' by {current_user.email}",
        user_id=current_user.id,
        user_email=current_user.email,
    )

    return GroupMemberRead(
        id=member.id,
        user_id=target_user.id,
        name=target_user.name,
        email=target_user.email,
        can_create=member.can_create,
        can_edit=member.can_edit,
        can_assign=member.can_assign,
        is_owner=(target_user.id == group.owner_id),
        joined_at=member.joined_at,
    )


@router.delete("/{group_id}/members/{user_id}")
def remove_group_member(
    group_id: str,
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Removes a member from the group (Owner only)."""
    group = get_group_or_404(group_id, session)
    check_group_owner(group, current_user)

    if user_id == group.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the group owner from the group.",
        )

    member = session.exec(
        select(GroupMember).where(
            GroupMember.group_id == group.id,
            GroupMember.user_id == user_id
        )
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member record not found.")

    session.delete(member)
    session.commit()
    return {"message": "Member removed from group successfully."}


@router.delete("/{group_id}")
def delete_group(
    group_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Permanently deletes a group and all its memberships (Owner only)."""
    group = get_group_or_404(group_id, session)
    check_group_owner(group, current_user)

    # Delete members
    members = session.exec(select(GroupMember).where(GroupMember.group_id == group.id)).all()
    for m in members:
        session.delete(m)

    group_name = group.name
    session.delete(group)
    session.commit()

    crud.record_audit_event(
        session=session,
        action="DELETE_GROUP",
        details=f"Group '{group_name}' deleted by {current_user.email}",
        user_id=current_user.id,
        user_email=current_user.email,
    )

    return {"message": f"Group '{group_name}' deleted successfully."}
