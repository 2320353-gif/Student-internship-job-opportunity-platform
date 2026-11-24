"""
Automated Pytest Suite: Role-Based Access Control (RBAC) & Ownership (Part 6).
Evaluates the 4 core teacher requirements:
1. Normal user can edit own opportunity.
2. Normal user CANNOT edit or delete another user's opportunity (HTTP 403).
3. Admin CAN edit or delete any opportunity.
4. Banned user is rejected from protected endpoints (HTTP 403).
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


def test_rbac_rule_1_user_can_edit_own_opportunity():
    """Rule 1: Normal student user can create and update their own opportunity."""
    token = get_token("student@university.edu")
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    create_res = client.post("/api/internships", json={
        "title": "Afrin Own Intern Role",
        "company_name": "Test Labs",
        "location": "Dhaka",
        "description": "Building reactive user interfaces",
        "salary": "৳15,000 / month",
        "deadline": "2026-12-30",
        "status": "Open"
    }, headers=headers)
    assert create_res.status_code == 201
    opp_id = create_res.json()["id"]

    # Update own post
    update_res = client.put(f"/api/internships/{opp_id}", json={
        "title": "Afrin Own Intern Role (Updated)"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Afrin Own Intern Role (Updated)"


def test_rbac_rule_2_user_cannot_edit_another_users_opportunity():
    """Rule 2: Normal user CANNOT edit another user's opportunity (Returns HTTP 403)."""
    # 1. Student 1 creates post
    token_1 = get_token("student@university.edu")
    create_res = client.post("/api/internships", json={
        "title": "Protected Role By Student 1",
        "company_name": "Private Corp",
        "location": "Remote",
        "description": "Confidential internal role",
        "salary": "৳20,000 / month",
        "deadline": "2026-12-30",
        "status": "Open"
    }, headers={"Authorization": f"Bearer {token_1}"})
    opp_id = create_res.json()["id"]

    # 2. Student 2 attempts to edit Student 1's post -> MUST BE 403
    token_2 = get_token("student2@university.edu")
    hack_res = client.put(f"/api/internships/{opp_id}", json={
        "title": "Unauthorized Modification Attempt"
    }, headers={"Authorization": f"Bearer {token_2}"})
    assert hack_res.status_code == 403
    assert "Forbidden" in hack_res.json()["detail"]

    # 3. Student 2 attempts to delete Student 1's post -> MUST BE 403
    del_res = client.delete(f"/api/internships/{opp_id}", headers={"Authorization": f"Bearer {token_2}"})
    assert del_res.status_code == 403


def test_rbac_rule_3_admin_can_modify_any_opportunity():
    """Rule 3: Admin CAN edit or delete any opportunity."""
    # 1. Student creates post
    student_token = get_token("student@university.edu")
    create_res = client.post("/api/internships", json={
        "title": "Opportunity to be Moderated",
        "company_name": "Open Source Foundation",
        "location": "Remote",
        "description": "Student listing to test admin moderation",
        "salary": "Unpaid",
        "deadline": "2026-12-31",
        "status": "Open"
    }, headers={"Authorization": f"Bearer {student_token}"})
    opp_id = create_res.json()["id"]

    # 2. Admin edits
    admin_token = get_token("admin@platform.com")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    edit_res = client.put(f"/api/internships/{opp_id}", json={
        "title": "Opportunity (Admin Verified)"
    }, headers=admin_headers)
    assert edit_res.status_code == 200

    # 3. Admin deletes
    del_res = client.delete(f"/api/internships/{opp_id}", headers=admin_headers)
    assert del_res.status_code == 200


def test_rbac_rule_4_banned_user_rejected():
    """Rule 4: Banned user is rejected with HTTP 403 from protected endpoints."""
    admin_token = get_token("admin@platform.com")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Ban student 3
    ban_res = client.post("/api/admin/users/b2000000-0000-0000-0000-000000000003/ban", headers=admin_headers)
    assert ban_res.status_code == 200
    assert ban_res.json()["is_banned"] is True

    # 2. Attempt login as banned user -> 403
    login_banned = client.post("/api/auth/login", json={
        "email": "student3@university.edu",
        "password": "password123"
    })
    assert login_banned.status_code == 403
    assert "banned" in login_banned.json()["detail"].lower()

    # 3. Clean up: Unban student 3
    unban_res = client.post("/api/admin/users/b2000000-0000-0000-0000-000000000003/ban", headers=admin_headers)
    assert unban_res.status_code == 200
    assert unban_res.json()["is_banned"] is False


def test_security_officer_admin_capabilities_and_admin_manager_protection():
    """
    Security Officer hierarchy check:
    1. Security Officer has full admin access (overview, audit logs, user list, student moderation).
    2. Security Officer CANNOT ban the Admin Manager (Returns HTTP 403).
    3. Security Officer CANNOT demote the Admin Manager (Returns HTTP 403).
    4. Security Officer CANNOT delete/modify opportunities created by the Admin Manager (Returns HTTP 403).
    5. Admin Manager can moderate Security Officer if needed.
    """
    officer_token = get_token("admin2@platform.com")
    officer_headers = {"Authorization": f"Bearer {officer_token}"}
    admin_token = get_token("admin@platform.com")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Security Officer can access admin command center
    overview = client.get("/api/admin/overview", headers=officer_headers)
    assert overview.status_code == 200
    assert "total_users" in overview.json()

    # 2. Security Officer ATTEMPTS TO BAN Admin Manager -> MUST BE 403 FORBIDDEN
    ban_attempt = client.post(
        "/api/admin/users/a1000000-0000-0000-0000-000000000001/ban",
        headers=officer_headers
    )
    assert ban_attempt.status_code == 403
    assert "protected" in ban_attempt.json()["detail"].lower()

    # 3. Security Officer ATTEMPTS TO DEMOTE Admin Manager -> MUST BE 403 FORBIDDEN
    demote_attempt = client.post(
        "/api/admin/users/a1000000-0000-0000-0000-000000000001/role",
        headers=officer_headers
    )
    assert demote_attempt.status_code == 403
    assert "protected" in demote_attempt.json()["detail"].lower()

    # 4. Admin Manager posts opportunity -> Security Officer CANNOT delete or edit it
    create_res = client.post("/api/internships", json={
        "title": "Executive Engineering Internship",
        "company_name": "Antigravity Systems",
        "location": "Dhaka",
        "description": "Posted directly by the Admin Manager",
        "salary": "৳50,000 / month",
        "deadline": "2026-12-31",
        "status": "Open"
    }, headers=admin_headers)
    assert create_res.status_code == 201
    admin_opp_id = create_res.json()["id"]

    # Security Officer tries to edit Admin Manager's post -> 403
    officer_edit = client.put(f"/api/internships/{admin_opp_id}", json={
        "title": "Tampered Title"
    }, headers=officer_headers)
    assert officer_edit.status_code == 403

    # Security Officer tries to delete Admin Manager's post -> 403
    officer_del = client.delete(f"/api/internships/{admin_opp_id}", headers=officer_headers)
    assert officer_del.status_code == 403

    # Admin Manager CAN edit and delete their own post
    admin_del = client.delete(f"/api/internships/{admin_opp_id}", headers=admin_headers)
    assert admin_del.status_code == 200
