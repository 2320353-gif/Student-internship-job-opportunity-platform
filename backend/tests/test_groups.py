"""
Automated Pytest Suite: Shared Groups & Collaboration (Part 6).
Evaluates group creation, permission enforcement, and owner restrictions.
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


def get_token(email: str, password: str = "password123") -> str:
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, f"Login failed for {email}"
    return res.json()["access_token"]


def test_create_and_manage_group():
    """Student creates a group, adds a member, and deletes it."""
    owner_token = get_token("student@university.edu")
    owner_headers = {"Authorization": f"Bearer {owner_token}"}

    # 1. Create group
    create_res = client.post("/api/groups", json={
        "name": "CSE309 Project Study Circle",
        "description": "Collaborative project group"
    }, headers=owner_headers)
    assert create_res.status_code == 201
    group_id = create_res.json()["id"]

    # 2. Non-owner (Student 2) tries to delete group -> MUST BE 403
    other_token = get_token("student2@university.edu")
    hack_del = client.delete(f"/api/groups/{group_id}", headers={"Authorization": f"Bearer {other_token}"})
    assert hack_del.status_code == 403

    # 3. Owner adds member with custom permissions
    add_member_res = client.post(f"/api/groups/{group_id}/members", json={
        "email": "student2@university.edu",
        "can_create": True,
        "can_edit": True,
        "can_assign": False
    }, headers=owner_headers)
    assert add_member_res.status_code == 201
    assert add_member_res.json()["can_edit"] is True

    # 4. Owner deletes group
    del_res = client.delete(f"/api/groups/{group_id}", headers=owner_headers)
    assert del_res.status_code == 200
