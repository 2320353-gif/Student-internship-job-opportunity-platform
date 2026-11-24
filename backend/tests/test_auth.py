"""
Automated Pytest Suite: Authentication & Token Lifecycle (Part 6).
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
for p in [str(BASE_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import main

client = TestClient(main.app)


def test_login_success():
    """Valid credentials return a valid JWT access token and refresh token."""
    res = client.post("/api/auth/login", json={
        "email": "student@university.edu",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "student@university.edu"


def test_login_invalid_password():
    """Incorrect password returns 401 Unauthorized."""
    res = client.post("/api/auth/login", json={
        "email": "student@university.edu",
        "password": "wrong_password_999"
    })
    assert res.status_code == 401
    assert "Incorrect email or password" in res.json()["detail"]


def test_register_duplicate_email():
    """Registering with an already existing email returns 400 Bad Request."""
    res = client.post("/api/auth/register", json={
        "name": "Duplicate Student",
        "email": "student@university.edu",
        "password": "password123"
    })
    assert res.status_code == 400
    assert "already exists" in res.json()["detail"]


def test_protected_route_without_token():
    """Accessing protected routes without token returns 401 Unauthorized."""
    res = client.get("/api/auth/me")
    assert res.status_code == 401


def test_protected_route_with_invalid_token():
    """Accessing protected routes with forged or invalid token returns 401 Unauthorized."""
    res = client.get("/api/auth/me", headers={"Authorization": "Bearer forged_invalid_token_xyz"})
    assert res.status_code == 401


def test_token_refresh():
    """Valid refresh token returns new access token."""
    login_res = client.post("/api/auth/login", json={
        "email": "student@university.edu",
        "password": "password123"
    })
    refresh_token = login_res.json()["refresh_token"]

    refresh_res = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()
