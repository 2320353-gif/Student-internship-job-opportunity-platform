# Student Internship & Job Opportunity Platform (OpportunityHub)
### CSE309 Final Project – Complete Web Application Architecture

A production-ready full-stack web application built for the **CSE309 Final Project Assessment**, featuring an **Internship Opportunity Manager** expanded with enterprise JWT authentication, Role-Based Access Control (RBAC), collaborative student groups, an administrator command center, immutable audit logs, automated test coverage, and Supabase PostgreSQL persistence.

---

## 🛠️ Complete Tech Stack

- **Frontend:** React 19, TypeScript, Vite, Modern Responsive Design System
- **Backend:** Python 3.12, FastAPI, SQLModel (SQLAlchemy 2.0 + Pydantic v2), PyJWT, Bcrypt
- **Database:** Supabase Managed PostgreSQL (Session Pooler) + Zero-Config Local SQLite Fallback
- **Testing:** Pytest & HTTPX Test Suite (12/12 test cases passing)
- **Deployment:** Vercel Serverless Ready (`vercel.json`)

---

## 🏛️ Project Architecture & Implemented Parts

### 🟢 Part 1 & 2: Authentication Engine & Login Gateway
- **Bcrypt Password Hashing:** 12-round salt hashing (`backend/auth/security.py`).
- **Dual-Token System:** 
  - 15-minute stateless `HS256` JWT access token.
  - 7-day cryptographically secure refresh token (`secrets.token_urlsafe(64)`).
- **Server-Side Token Revocation:** Refresh tokens are hashed via SHA-256 and stored in the `refresh_tokens` table. Logging out sets `is_revoked = True`.
- **Frontend Gateway:** `LoginPage.tsx` gates all access until authentication is established, with one-click demo login buttons.

### 🟢 Part 3: Role-Based Access Control (RBAC) & Post Ownership
- **Ownership Binding:** `Internship.user_id` foreign key permanently binds opportunities to their creators.
- **Frontend Permission Guard:** `InternshipCard.tsx` calculates `canModify` to conditionally hide Edit/Delete buttons and show "👁 View Details (Read-Only)".
- **Backend Security Guard:** `backend/routers/internships.py` strictly returns `HTTP 403 Forbidden` if a student attempts to modify or delete another user's post.

### 🟢 Part 4: Shared Groups & Collaboration
- **Team Workspaces:** Students can create hiring squads and teams (`Group` and `GroupMember` tables).
- **Granular Permissions:** Supports `can_create`, `can_edit`, and `can_assign` member permission flags.
- **Frontend Modal:** `GroupManagementModal.tsx` for member invitations, permission toggles, and group feed filtering.

### 🟢 Part 5: Admin Command Center & Role Hierarchy
- **Executive Dashboard:** `AdminDashboardModal.tsx` with 4 dedicated tabs:
  1. *Platform Overview:* Live KPI summary cards (Total Users, Active Posts, Banned Users, Shared Groups).
  2. *User Directory:* Searchable, filterable table to toggle account bans and promote/demote roles.
  3. *Security Audit Trail:* Real-time chronological audit trail of all authentication and moderation actions.
  4. *Data Export:* One-click CSV export of platform data.
- **Admin Hierarchy & Protection:** **Admin Manager** (`admin@platform.com` / `is_main_admin=True`) is permanently protected from bans and demotions. The **Security Officer** (`admin2@platform.com`) has moderation capabilities but cannot modify the Admin Manager.
- **Instant Session Invalidation:** Banning a user immediately revokes all their active refresh tokens in the database.

### 🟢 Part 6: Automated Testing & Cloud Persistence
- **Automated Test Suite:** 12 comprehensive unit and integration tests in `backend/tests/` testing password security, JWT expiration, RBAC ownership, group management, and role hierarchies.
- **Supabase Cloud Database:** Connected to PostgreSQL pooler at `aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres`.

---

## 👥 Pre-Seeded Academic Evaluation Accounts

| Role | Email | Password | Permissions & Boundaries |
| :--- | :--- | :--- | :--- |
| **Admin Manager (Root)** | `admin@platform.com` | `admin123` | Full administrative control; permanently immune to bans and demotions |
| **Security Officer** | `admin2@platform.com` | `admin123` | Can moderate standard users; cannot ban Admin Manager or edit their posts |
| **Student 1 (Owner)** | `student1@university.edu` | `student123` | Post creator & Group Owner; full control over own postings |
| **Student 2 (Collaborator)** | `student2@university.edu` | `student123` | Group member with collaborative edit permissions |
| **Student 3 (Viewer)** | `student3@university.edu` | `student123` | Standard user with read-only view on non-owned postings |

---

## 🧪 Running Automated Tests

Run the backend test suite:
```bash
cd backend
pytest tests/ -v
```
Expected output:
```text
====================== 12 passed in 30.23s =======================
```

---

## 🚀 Running the Project Locally

### 1. Run Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```
*API Base: `http://localhost:8000` | Swagger Docs: `http://localhost:8000/docs`*

### 2. Run Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
*App URL: `http://localhost:5173`*
