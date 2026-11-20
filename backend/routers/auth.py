"""
Authentication router: Signup, Login, Token Refresh, Logout, and Profile management.
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

try:
    from database import get_session
    from models import (
        RefreshToken,
        Token,
        TokenRefreshRequest,
        User,
        UserCreate,
        UserLogin,
        UserRead,
        UserRole,
        UserUpdate,
    )
    from auth.security import (
        ACCESS_TOKEN_EXPIRE_MINUTES,
        REFRESH_TOKEN_EXPIRE_DAYS,
        create_access_token,
        create_refresh_token,
        hash_password,
        hash_token,
        verify_password,
    )
    from auth.dependencies import get_current_active_user
except ImportError:
    from backend.database import get_session
    from backend.models import (
        RefreshToken,
        Token,
        TokenRefreshRequest,
        User,
        UserCreate,
        UserLogin,
        UserRead,
        UserRole,
        UserUpdate,
    )
    from backend.auth.security import (
        ACCESS_TOKEN_EXPIRE_MINUTES,
        REFRESH_TOKEN_EXPIRE_DAYS,
        create_access_token,
        create_refresh_token,
        hash_password,
        hash_token,
        verify_password,
    )
    from backend.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user account and return JWT tokens."""
    clean_email = user_data.email.strip().lower()
    if "@" not in clean_email or "." not in clean_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )

    existing_user = session.exec(select(User).where(User.email == clean_email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )

    assigned_role = UserRole.ADMIN.value if clean_email.startswith("admin@") else UserRole.USER.value

    new_user = User(
        name=user_data.name.strip(),
        email=clean_email,
        hashed_password=hash_password(user_data.password),
        role=assigned_role,
        is_banned=False,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    access_token = create_access_token(
        data={"sub": new_user.id, "email": new_user.email, "role": new_user.role}
    )
    raw_refresh = create_refresh_token(new_user.id)
    refresh_hash = hash_token(raw_refresh)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).strftime("%Y-%m-%d %H:%M:%S")

    token_record = RefreshToken(
        user_id=new_user.id,
        token_hash=refresh_hash,
        expires_at=expires_at,
        is_revoked=False,
    )
    session.add(token_record)
    session.commit()

    user_read = UserRead(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        role=new_user.role,
        is_banned=new_user.is_banned,
        created_at=new_user.created_at,
    )

    return Token(
        access_token=access_token,
        refresh_token=raw_refresh,
        token_type="bearer",
        user=user_read,
    )


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user with email and password and return JWT tokens."""
    clean_email = credentials.email.strip().lower()
    user = session.exec(select(User).where(User.email == clean_email)).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been suspended or banned. Please contact administration."
        )

    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    raw_refresh = create_refresh_token(user.id)
    refresh_hash = hash_token(raw_refresh)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).strftime("%Y-%m-%d %H:%M:%S")

    token_record = RefreshToken(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=expires_at,
        is_revoked=False,
    )
    session.add(token_record)
    session.commit()

    user_read = UserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        is_banned=user.is_banned,
        created_at=user.created_at,
    )

    return Token(
        access_token=access_token,
        refresh_token=raw_refresh,
        token_type="bearer",
        user=user_read,
    )


@router.post("/refresh", response_model=Token)
def refresh_session(token_request: TokenRefreshRequest, session: Session = Depends(get_session)):
    """Issue a new access token using a valid, unrevoked refresh token."""
    raw_refresh = token_request.refresh_token
    token_hash = hash_token(raw_refresh)

    token_record = session.exec(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False
        )
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token"
        )

    expires_dt = datetime.strptime(token_record.expires_at, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_dt:
        token_record.is_revoked = True
        session.add(token_record)
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again."
        )

    user = session.exec(select(User).where(User.id == token_record.user_id)).first()
    if not user or user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or account is suspended"
        )

    new_access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )

    user_read = UserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        is_banned=user.is_banned,
        created_at=user.created_at,
    )

    return Token(
        access_token=new_access_token,
        refresh_token=raw_refresh,
        token_type="bearer",
        user=user_read,
    )


@router.post("/logout")
def logout(token_request: TokenRefreshRequest, session: Session = Depends(get_session)):
    """Revoke a refresh token on logout to terminate the session."""
    token_hash = hash_token(token_request.refresh_token)
    token_record = session.exec(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    ).first()

    if token_record:
        token_record.is_revoked = True
        session.add(token_record)
        session.commit()

    return {"status": "success", "message": "Session invalidated and logged out successfully"}


@router.get("/me", response_model=UserRead)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Get profile information for currently authenticated user."""
    return UserRead(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        is_banned=current_user.is_banned,
        created_at=current_user.created_at,
    )


@router.put("/profile", response_model=UserRead)
def update_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update user name or password with verification."""
    if updates.name and updates.name.strip():
        current_user.name = updates.name.strip()

    if updates.new_password:
        if not updates.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to set a new password"
            )
        if not verify_password(updates.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password verification failed"
            )
        if len(updates.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long"
            )
        current_user.hashed_password = hash_password(updates.new_password)

    current_user.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return UserRead(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        is_banned=current_user.is_banned,
        created_at=current_user.created_at,
    )
