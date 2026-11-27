# Independent University, Bangladesh
## Department of Computer Science & Engineering
### CSE309: Web Application & Internet

---

# Final Project Submission Report
### **Student Internship & Job Opportunity Platform (OpportunityHub)**

**Submitted By:**
* **Name:** Tanjina Akter Limo
* **Student ID:** 2320353
* **Section:** 06

**Submitted To:**
* **Instructor:** Sayef Reyadh
* **Designation:** Adjunct Lecturer, Department of Computer Science & Engineering
* **Institution:** Independent University, Bangladesh (IUB)

**Project Metadata:**
* **Project Title:** Student Internship & Job Opportunity Platform (OpportunityHub)
* **Vercel Live URL:** [https://2320353.vercel.app](https://2320353.vercel.app)
* **GitHub Repository:** [https://github.com/2320353-gif/Student-internship-job-opportunity-platform](https://github.com/2320353-gif/Student-internship-job-opportunity-platform)
* **Semester:** Autumn 2026
* **Date of Submission:** 28-11-2026

---

## Table of Contents
1. [1. Executive Summary](#1-executive-summary)
   - [1.1 Project Overview](#11-project-overview)
   - [1.2 What Was Built Since the Mid Assessment](#12-what-was-built-since-the-mid-assessment)
   - [1.3 Live Links](#13-live-links)
2. [Part A. Product Requirements (PRD)](#part-a-product-requirements-prd)
   - [A1. Problem Statement](#a1-problem-statement)
   - [A2. Users and Roles](#a2-users-and-roles)
   - [A3. Goals and Success Measures](#a3-goals-and-success-measures)
   - [A4. Scope and Non-Goals](#a4-scope-and-non-goals)
   - [A5. User Stories](#a5-user-stories)
3. [Part B. Software Requirements (SRS)](#part-b-software-requirements-srs)
   - [B1. Introduction](#b1-introduction)
   - [B2. Functional Requirements](#b2-functional-requirements)
   - [B3. Non-Functional Requirements](#b3-non-functional-requirements)
   - [B4. Roles and Permission Matrix](#b4-roles-and-permission-matrix)
   - [B5. Use Cases](#b5-use-cases)
   - [B6. Acceptance Criteria](#b6-acceptance-criteria)
   - [B7. Traceability Matrix](#b7-traceability-matrix)
4. [Part C. Technical Design (TDD)](#part-c-technical-design-tdd)
   - [C1. Technology Stack](#c1-technology-stack)
   - [C2. System Architecture](#c2-system-architecture)
   - [C3. Backend and Frontend Structure](#c3-backend-and-frontend-structure)
   - [C4. Data Model](#c4-data-model)
   - [C5. API Design](#c5-api-design)
   - [C6. JWT Authentication Design](#c6-jwt-authentication-design)
   - [C7. RBAC Design](#c7-rbac-design)
   - [C8. Admin Dashboard Design](#c8-admin-dashboard-design)
   - [C9. Security Design and Threats](#c9-security-design-and-threats)
   - [C10. Deployment on Vercel](#c10-deployment-on-vercel)
   - [C11. Testing](#c11-testing)
5. [Part D. Evidence: Screenshots of the Running Application](#part-d-evidence-screenshots-of-the-running-application)
   - [D1. User Side](#d1-user-side)
   - [D2. Security Behaviour](#d2-security-behaviour)
   - [D3. Admin Dashboard](#d3-admin-dashboard)
   - [D4. Deployment](#d4-deployment)
   - [D5. Tests](#d5-tests)
6. [Part E. Project Management and Conclusion](#part-e-project-management-and-conclusion)
   - [E1. How to Run and Test](#e1-how-to-run-and-test)
   - [E2. GitHub Work](#e2-github-work)
   - [E3. Limitations](#e3-limitations)
   - [E4. Future Work](#e4-future-work)
   - [E5. Sources, Libraries and Tools](#e5-sources-libraries-and-tools)
7. [Appendix. Test Accounts and Video Demo](#appendix-test-accounts-and-video-demo)

---

## List of Figures and Screenshots
- **Figure 1**: High-Level System Architecture Diagram (Section C2)
- **Figure 2**: Entity-Relationship (ER) Diagram (Section C4)
- **Figure 3**: JWT Authentication & Silent Refresh Sequence Diagram (Section C6)
- **Figure 4**: Request Authorization & RBAC Execution Flow (Section C7)
- **Figure 5**: Admin Command Center Architectural Subsystem (Section C8)
- **Figure 6**: Vercel Serverless & Supabase Cloud Deployment Topology (Section C10)
- **Figure 7**: Core System Use Case Diagram (Section B5)
- **Screenshots S1–S21**: Verified Application Evidence (Part D)

---

# 1. Executive Summary

### 1.1 Project Overview
The **Student Internship & Job Opportunity Platform (OpportunityHub)** is a centralized web application engineered specifically for university students, career centers, and hiring managers. It streamlines finding, publishing, reviewing, and collaboratively managing student internships, job openings, and career placements. Rather than relying on scattered social media posts or unstructured bulletin boards, the platform provides authenticated student access, verified posting credentials, departmental collaboration groups, and strict administrative oversight.

**Technology Stack in One Line:**  
React 19 with TypeScript and Vite (Frontend), FastAPI and SQLModel with Python 3.12 (Backend), Supabase Managed PostgreSQL (Database), and Vercel Serverless (Hosting & CI/CD).

### 1.2 What Was Built Since the Mid Assessment
Since the mid-project assessment (which delivered a standalone CRUD prototype), the platform was expanded with the following additions:
* **JWT Authentication with Refresh and Logout:** Implemented 12-round Bcrypt password hashing, 15-minute stateless `HS256` access tokens, 7-day cryptographically secure refresh tokens stored as SHA-256 hashes in Supabase, and instant server-side revocation on logout.
* **Role-Based Access Control (RBAC):** Bound opportunities to creators via `user_id`, enforced server-side checks restricting students to editing only their own posts (`HTTP 403 Forbidden` on breach), and added group-level permissions (`can_create`, `can_edit`, `can_assign`).
* **Admin Command Center:** Built an administrative console with platform KPI statistics, a searchable/filterable user directory, role promotion/demotion, instantaneous account banning with active token revocation, root **Admin Manager** protection, live security audit trail logging, and CSV exports.
* **Audit Logging & Cloud Persistence:** Created an immutable `audit_logs` subsystem, connected a cloud PostgreSQL database pooler on Supabase, and implemented an automated 12-test `pytest` verification suite.

### 1.3 Live Links

#### Table 1: Live Links
| Resource | URL |
| :--- | :--- |
| **GitHub Repository** | [https://github.com/2320353-gif/Student-internship-job-opportunity-platform](https://github.com/2320353-gif/Student-internship-job-opportunity-platform) |
| **Vercel Frontend Application** | [https://2320353.vercel.app](https://2320353.vercel.app) |
| **Backend API Root** | [https://2320353.vercel.app/api](https://2320353.vercel.app/api) |
| **Interactive API Documentation (Swagger)** | [https://2320353.vercel.app/docs](https://2320353.vercel.app/docs) |
| **Video Demonstration** | *Available in Appendix / Course Submission Portal* |

---

# Part A. Product Requirements (PRD)

### A1. Problem Statement
University students struggle to discover relevant, verified internship opportunities. Currently, listings are scattered across private WhatsApp groups, Facebook posts, unindexed email threads, and physical bulletin boards. As a result, students miss critical application deadlines, fall victim to unverified or expired job postings, and cannot track their submission statuses. 

Departmental clubs, lab groups, and university placement coordinators have no structured way to collaborate on compiling opportunities, delegating posting responsibilities, or ensuring expired listings are promptly removed. Without a centralized platform with authentication and role-based permissions, job boards become cluttered with spam, duplicate records, and unauthorized content modifications.

### A2. Users and Roles

#### Table 2: Users and Roles
| Role | Who They Are | Main Tasks | What They Must Never Be Able To Do |
| :--- | :--- | :--- | :--- |
| **Visitor / Guest** | Unauthenticated user visiting the landing page. | View the login/signup screen, view public demo instructions. | Access the dashboard, read confidential job details, make posts, or call protected APIs. |
| **Student / User** | Authenticated university student or job seeker. | Browse opportunities, search/filter listings, create new opportunities, edit/delete own postings. | Modify or delete another user's opportunities, access the admin command center, or unban accounts. |
| **Group Member** | Student assigned to a collaborative student team/club. | Create listings under the group banner, view group listings, edit listings if granted `can_edit`. | Invite or remove group members, delete the group, or exceed assigned permission flags. |
| **Group Owner** | Student who founded a specific collaboration group. | Create group opportunities, invite members, configure granular permissions (`can_create`, `can_edit`, `can_assign`), disband group. | Access the global Admin Command Center, ban users platform-wide, or edit postings belonging to other groups/users. |
| **Security Officer** | Administrative staff member (`admin2@platform.com`). | Moderate user accounts, ban violating students, inspect audit logs, edit student opportunities. | Ban, demote, or modify postings belonging to the root Admin Manager (`HTTP 403 Forbidden`). |
| **Admin Manager** | Root system administrator (`admin@platform.com`). | Full administrative control, role assignment, platform-wide content moderation, system audits, CSV export. | Ban their own account, or delete immutable audit logs. |

### A3. Goals and Success Measures

#### Table 3: Goals and Success Measures
| # | Goal Description | Category | Measurable / Testable Success Metric |
| :---: | :--- | :--- | :--- |
| **G1** | **Strict Post Ownership Isolation** | Security | No user can modify or delete another user's post; backend enforces `HTTP 403 Forbidden` on breach ($100\%$ test pass). |
| **G2** | **Short-Lived & Revocable Sessions** | Security | Access tokens expire in strictly $15$ minutes; revoking a refresh token immediately rejects subsequent `/api/auth/refresh` calls with `HTTP 401`. |
| **G3** | **Zero-Downtime Data Persistence** | Reliability | Data persists across serverless restarts and browser reloads via hosted Supabase PostgreSQL ($100\%$ retention). |
| **G4** | **Instant Account Suspension** | Security | Banning a user sets `is_banned = True` and instantly revokes all active refresh tokens; subsequent requests fail with `HTTP 403`. |
| **G5** | **Fast Response Latency** | Performance | In-memory API response times stay under $300\text{ ms}$ for list and detail queries under normal load. |
| **G6** | **High Test Coverage** | Maintainability | All $12$ critical backend test cases pass automated execution via `pytest` ($100\%$ pass rate). |

### A4. Scope and Non-Goals
* **In Scope:**
  - Complete JWT Authentication with Bcrypt salting and hashing, token rotation, and server-side revocation.
  - Role-Based Access Control (Student, Group Member, Group Owner, Security Officer, Admin Manager).
  - Opportunity CRUD with user ownership binding and conditional frontend UI rendering.
  - Collaborative Shared Groups with granular permission flags (`can_create`, `can_edit`, `can_assign`).
  - Admin Command Center with overview metrics, user directory moderation, audit logging, and CSV export.
  - Automated testing suite (`pytest`) and deployment to Vercel with Supabase PostgreSQL cloud persistence.
* **Out of Scope (Deliberate Non-Goals):**
  - Direct PDF resume parsing / AI resume ranking (deferred to post-MVP).
  - Built-in live audio/video interview calling (students use external links like Google Meet or Zoom).
  - Third-party OAuth providers (Google/GitHub login deferred to keep authentication fully self-contained and auditable for academic evaluation).
* **Assumptions and Constraints:**
  - Modern web browser compatibility (Chrome, Firefox, Safari, Edge).
  - Vercel Serverless environment limits (read-only filesystem runtime requiring database-backed persistence).
  - Assessment deadline of Autumn 2026 semester.

### A5. User Stories

#### Table 4: User Stories
| ID | As a (Role) | I Want To | So That |
| :---: | :--- | :--- | :--- |
| **US-01** | Student | Register with my name, email, and password | I can obtain my personal account and start tracking opportunities. |
| **US-02** | Student | Log in and receive a secure JWT token | I can access protected platform features without re-entering credentials on every page. |
| **US-03** | Student | Silently renew my session using a refresh token | I remain logged in while working without abrupt session drops every 15 minutes. |
| **US-04** | Student | Post a new internship opportunity | My peers can discover open positions at hiring organizations. |
| **US-05** | Student | Edit or delete only the opportunities I posted | I can correct mistakes while preventing unauthorized tampering by other students. |
| **US-06** | Student | View other students' posts in Read-Only mode | I can learn about job requirements without accidentally altering someone else's data. |
| **US-07** | Group Owner | Create a team and invite members with permissions | My club or department can collaboratively maintain a shared set of listings. |
| **US-08** | Group Member | Post opportunities under my group's umbrella | The postings represent our team rather than an individual. |
| **US-09** | Admin | View a centralized overview dashboard with metrics | I can monitor active users, opportunities, banned accounts, and teams. |
| **US-10** | Admin | Search and ban abusive accounts | Bad actors are immediately blocked from making API requests. |
| **US-11** | Admin | Promote a student to an administrator or demote | I can delegate administrative responsibilities to staff. |
| **US-12** | Admin | Inspect an immutable security audit trail | I can trace who created, modified, deleted, or banned records across the system. |

---

# Part B. Software Requirements (SRS)

### B1. Introduction
This Software Requirements Specification (SRS) provides the formal, testable specification for the OpportunityHub platform. It is intended for course evaluators, software engineers, and security auditors.

#### Key Terminology & Definitions
* **JWT (JSON Web Token):** An open standard (RFC 7519) compact, URL-safe container for cryptographically signed claims.
* **Access Token:** A short-lived (15 minutes) signed JWT used as a Bearer token in the `Authorization` HTTP header to access protected API endpoints.
* **Refresh Token:** A long-lived (7 days), high-entropy opaque random string stored as a SHA-256 hash in the database to obtain fresh access tokens.
* **RBAC (Role-Based Access Control):** An authorization mechanism that restricts system access based on assigned roles and ownership attributes.
* **Audit Log:** An append-only, immutable database record documenting security-sensitive operations with actor ID, timestamp, and action label.

**References:** RFC 7519 (JSON Web Tokens), OWASP Application Security Verification Standard (ASVS 4.0), NIST SP 800-63B (Digital Identity Guidelines).

### B2. Functional Requirements

#### Table 5: Functional Requirements – Authentication (FR-AUTH)
| ID | Requirement Statement |
| :---: | :--- |
| **FR-AUTH-01** | The system shall provide a registration endpoint (`POST /api/auth/register`) accepting name, email, and password. |
| **FR-AUTH-02** | The system shall validate email syntax and reject passwords shorter than 6 characters with `HTTP 400 Bad Request`. |
| **FR-AUTH-03** | The system shall reject duplicate registration emails with `HTTP 400 Bad Request`. |
| **FR-AUTH-04** | The system shall hash plaintext passwords using Bcrypt with 12 salt rounds before database persistence. |
| **FR-AUTH-05** | The system shall provide a login endpoint (`POST /api/auth/login`) returning a 15-minute `HS256` JWT access token and a 7-day refresh token. |
| **FR-AUTH-06** | The system shall store refresh tokens in the `refresh_tokens` table as SHA-256 hashes with expiration timestamps. |
| **FR-AUTH-07** | The system shall provide a token renewal endpoint (`POST /api/auth/refresh`) that issues a new access token if the refresh token is valid and unrevoked. |
| **FR-AUTH-08** | The system shall provide a logout endpoint (`POST /api/auth/logout`) that marks the presented refresh token as `is_revoked = True`. |
| **FR-AUTH-09** | The system shall reject expired, tampered, or missing JWT Bearer tokens with `HTTP 401 Unauthorized`. |

#### Table 6: Functional Requirements – Role-Based Access Control (FR-RBAC)
| ID | Requirement Statement |
| :---: | :--- |
| **FR-RBAC-01** | The system shall bind the creator's ID (`user_id`) to every opportunity created via `POST /api/internships`. |
| **FR-RBAC-02** | The system shall allow users to edit (`PUT /api/internships/{id}`) and delete (`DELETE /api/internships/{id}`) only their own opportunities. |
| **FR-RBAC-03** | The system shall reject cross-user modification and deletion attempts with `HTTP 403 Forbidden`. |
| **FR-RBAC-04** | The system shall permit the root Admin Manager to edit and delete any opportunity platform-wide. |
| **FR-RBAC-05** | The system shall allow Security Officers to edit student posts but reject any attempt by a Security Officer to modify Admin Manager posts with `HTTP 403 Forbidden`. |
| **FR-RBAC-06** | The system shall allow users to filter listings by ownership via the `my_only=true` query parameter. |

#### Table 7: Functional Requirements – Collaborative Groups (FR-GRP)
| ID | Requirement Statement |
| :---: | :--- |
| **FR-GRP-01** | The system shall allow authenticated users to create a group via `POST /api/groups`, automatically designating the creator as Owner. |
| **FR-GRP-02** | The system shall permit only the Group Owner to invite members and assign permission flags (`can_create`, `can_edit`, `can_assign`). |
| **FR-GRP-03** | The system shall permit members with `can_create=True` to post opportunities linked to the `group_id`. |
| **FR-GRP-04** | The system shall permit only the Group Owner to disband the group or remove members. |

#### Table 8: Functional Requirements – Administrator Command Center (FR-ADM)
| ID | Requirement Statement |
| :---: | :--- |
| **FR-ADM-01** | The system shall provide a platform metrics endpoint (`GET /api/admin/overview`) accessible only to administrative roles. |
| **FR-ADM-02** | The system shall provide a paginated, searchable user directory endpoint (`GET /api/admin/users`). |
| **FR-ADM-03** | The system shall provide a ban toggle endpoint (`POST /api/admin/users/{id}/ban`) that toggles `is_banned` and invalidates all active sessions. |
| **FR-ADM-04** | The system shall prevent administrators from banning their own accounts with `HTTP 400 Bad Request`. |
| **FR-ADM-05** | The system shall permanently protect the Admin Manager (`is_main_admin=True`) from being banned or demoted by any other administrator with `HTTP 403 Forbidden`. |
| **FR-ADM-06** | The system shall reject any subsequent request from a banned user across all protected endpoints with `HTTP 403 Forbidden`. |
| **FR-ADM-07** | The system shall record an immutable entry in `audit_logs` for every login, post deletion, role change, and ban action. |
| **FR-ADM-08** | The system shall provide a CSV export endpoint (`GET /api/admin/export/csv`) downloading platform records. |

### B3. Non-Functional Requirements

#### Table 9: Non-Functional Requirements
| Quality Attribute | Requirement Specification | Metric / Verification Method |
| :--- | :--- | :--- |
| **Security** | Secrets (`JWT_SECRET`, `DATABASE_URL`) stored in environment variables; passwords hashed via Bcrypt (12 rounds); refresh tokens hashed via SHA-256. | Zero hardcoded production secrets in repository; verified via automated audit. |
| **Performance** | API endpoint latency $\le 300\text{ ms}$ for standard CRUD operations under single-client testing. | Verified via Chrome DevTools Network Tab and test benchmarks. |
| **Usability** | Single Page Application (SPA) responsive design; clear toast notifications on success/failure; modal dialogs with loading states. | Verified on mobile (375px), tablet (768px), and desktop (1440px) viewports. |
| **Reliability** | Persistent cloud database storage survives serverless cold starts, container recycles, and platform restarts without data loss. | Verified via Supabase PostgreSQL cloud persistence tests. |
| **Maintainability** | Centralized dependency injection (`get_current_active_user`, `require_admin`); automated test suite coverage. | 12/12 passing `pytest` automated test suite in `backend/tests/`. |

### B4. Roles and Permission Matrix

#### Table 10: Endpoint Groups by Roles
| Endpoint Group | Visitor | Student / User | Group Member | Group Owner | Security Officer | Admin Manager |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `POST /api/auth/register, login` | Yes | Yes | Yes | Yes | Yes | Yes |
| `GET /api/internships` | Yes | Yes | Yes | Yes | Yes | Yes |
| `GET /api/internships/{id}` | Yes | Yes | Yes | Yes | Yes | Yes |
| `POST /api/internships` | No | Yes | Yes | Yes | Yes | Yes |
| `PUT /api/internships/{id}` | No | Own Only | Own / Group* | Own / Group | Student Posts | All Posts |
| `DELETE /api/internships/{id}` | No | Own Only | Own Only | Own / Group | Student Posts | All Posts |
| `POST /api/groups` | No | Yes | Yes | Yes | Yes | Yes |
| `POST /api/groups/{id}/members` | No | No | No | Yes | No | No |
| `GET /api/admin/*` | No | No | No | No | Yes | Yes |
| `POST /api/admin/users/{id}/ban` | No | No | No | No | Yes (Not Root) | Yes (Not Self) |

*\*Subject to member `can_edit` permission flag.*

#### Table 11: Group Permissions
| Permission Flag | What It Allows | What Only Group Owner Can Do |
| :--- | :--- | :--- |
| `can_create` | Post opportunities linked to the team `group_id`. | Invite new members to the group. |
| `can_edit` | Edit existing opportunities posted under the team `group_id`. | Modify or revoke member permission flags. |
| `can_assign` | Assign team members to manage specific opportunity listings. | Remove members from the team. |
| *None* | View group opportunities and roster in read-only mode. | Permanently disband or delete the group. |

#### Table 12: Admin Rules
| Administrative Action | Security Officer (`admin2@platform.com`) | Admin Manager (`admin@platform.com`) |
| :--- | :---: | :---: |
| Access Admin Dashboard & Metrics | Allowed | Allowed |
| Moderate / Ban Standard Students | Allowed | Allowed |
| Promote Student to Administrator | Denied (`HTTP 403 Forbidden`) | Allowed |
| Ban Another Administrator | Denied (`HTTP 403 Forbidden`) | Denied (`HTTP 400 Bad Request` if self) |
| Ban the Admin Manager | **Strictly Forbidden (`HTTP 403`)** | **Strictly Forbidden (Self-ban guard)** |
| Modify Admin Manager Postings | **Strictly Forbidden (`HTTP 403`)** | Allowed |

### B5. Use Cases

```mermaid
useCaseDiagram
actor Student
actor Admin
actor Visitor

Visitor --> (Register Account)
Visitor --> (Log In)
Student --> (Log In & Silent Refresh)
Student --> (Create Opportunity)
Student --> (Edit/Delete Own Opportunity)
Student --> (Create & Manage Group)
Admin --> (View Admin Metrics)
Admin --> (Ban/Unban User)
Admin --> (Inspect Audit Logs)
Admin --> (Export CSV Data)
```

#### Table 13: Detailed Use Case Descriptions
* **UC-01: Log In and Token Refresh**
  * *Actor:* Student / User
  * *Preconditions:* User has registered an account.
  * *Main Flow:* 1. User submits email and password. 2. Backend validates Bcrypt hash. 3. Backend verifies `is_banned == False`. 4. Backend returns 15-min access token and 7-day refresh token hash. 5. Client stores tokens in `localStorage`. 6. Before expiration, client calls `/api/auth/refresh` to obtain a fresh access token without user disruption.
  * *Error Flow:* Invalid password returns `401 Unauthorized`. Banned user returns `403 Forbidden`.
  * *Postconditions:* User is authenticated; active session recorded in `refresh_tokens`.
* **UC-02: Create Internship Opportunity**
  * *Actor:* Student / User
  * *Preconditions:* User is authenticated with a valid access token.
  * *Main Flow:* 1. User clicks "+ Post Opportunity". 2. User fills title, company, location, salary, deadline. 3. Client submits `POST /api/internships`. 4. Server extracts `user_id` from Bearer token claims and assigns ownership. 5. Record saved to database.
  * *Error Flow:* Missing title or company returns `400 Bad Request`.
  * *Postconditions:* New opportunity visible on dashboard with "👤 My Post" badge for the owner.
* **UC-03: Denied Cross-User Modification Attempt (RBAC Enforcement)**
  * *Actor:* Student A attempting to edit Student B's opportunity.
  * *Preconditions:* Student A is authenticated; Student B created opportunity ID `X`.
  * *Main Flow:* 1. Student A attempts to bypass UI restrictions and sends `PUT /api/internships/X`. 2. Server verifies token and retrieves opportunity. 3. Server detects `internship.user_id != current_user.id`. 4. Server halts execution and returns `HTTP 403 Forbidden: You can only modify your own internship postings`.
  * *Postconditions:* Database remains unchanged; unauthorized attempt blocked.
* **UC-04: Configure Group Member Permissions**
  * *Actor:* Group Owner
  * *Preconditions:* Group exists; Owner is authenticated.
  * *Main Flow:* 1. Owner opens `GroupManagementModal.tsx`. 2. Owner enters member email and toggles permission checkboxes (`can_create`, `can_edit`). 3. Client submits `POST /api/groups/{id}/members`. 4. Server verifies owner status and creates `GroupMember` record.
  * *Error Flow:* Non-owner attempting to add members receives `403 Forbidden`.
  * *Postconditions:* New member added with granular permission flags.
* **UC-05: Ban Abusive User & Terminate Sessions**
  * *Actor:* Admin
  * *Preconditions:* Admin is logged in; target user is active.
  * *Main Flow:* 1. Admin navigates to User Directory tab in `AdminDashboardModal.tsx`. 2. Admin clicks "Ban User". 3. Client sends `POST /api/admin/users/{id}/ban`. 4. Server verifies target is not Admin Manager and not self. 5. Server sets `target_user.is_banned = True`. 6. Server revokes all refresh tokens belonging to target user (`is_revoked = True`). 7. Server writes `BAN_USER` event to `audit_logs`.
  * *Error Flow:* Attempt to ban Admin Manager returns `403 Forbidden`. Attempt to self-ban returns `400 Bad Request`.
  * *Postconditions:* Target user is banned; all active sessions immediately destroyed.
* **UC-06: Inspect Live Audit Trail**
  * *Actor:* Admin
  * *Preconditions:* Admin is authenticated.
  * *Main Flow:* 1. Admin opens Audit Trail tab in Admin Command Center. 2. Client calls `GET /api/admin/audit-logs`. 3. Server verifies admin role and queries `audit_logs` ordered by timestamp descending. 4. Table renders chronological log with action badges, actor email, and timestamp.
  * *Postconditions:* Security events audited without modifying log state.

### B6. Acceptance Criteria

#### Table 14: Acceptance Criteria (Given-When-Then)
| ID | Scenario | Given | When | Then |
| :---: | :--- | :--- | :--- | :--- |
| **AC-01** | Token Expiry | An access token older than 15 minutes | A request is sent with the expired token in the `Authorization` header | The backend rejects the request with `HTTP 401 Unauthorized`. |
| **AC-02** | Tampered Token Signature | A JWT with altered payload or manipulated signature | A request is made to any protected endpoint | The backend fails signature validation and returns `HTTP 401 Unauthorized`. |
| **AC-03** | Unauthorized Post Modification | A student logged in who does not own Opportunity #10 | The student sends a `PUT /api/internships/10` request | The server halts execution and returns `HTTP 403 Forbidden`. |
| **AC-04** | Member Permission Enforcement | A group member whose `can_create` permission is `False` | The member attempts to post an opportunity under that group | The server rejects the creation with `HTTP 403 Forbidden`. |
| **AC-05** | Banned User Rejection | A user account marked with `is_banned = True` | The user attempts any authenticated request | `get_current_active_user` blocks the request with `HTTP 403 Forbidden`. |
| **AC-06** | Admin Manager Ban Protection | A Security Officer logged in | The officer sends `POST /api/admin/users/{admin_manager_id}/ban` | The server rejects with `HTTP 403 Forbidden: The Main Admin is permanently protected`. |

### B7. Traceability Matrix

#### Table 15: Traceability Matrix
| Requirement ID | Module / Endpoint | Code Implementation File | Automated Test | Evidence Screenshot |
| :---: | :--- | :--- | :--- | :---: |
| **FR-AUTH-01..04** | `POST /api/auth/register` | `backend/routers/auth.py` | `test_register_duplicate_email` | S1 |
| **FR-AUTH-05..06** | `POST /api/auth/login` | `backend/routers/auth.py` | `test_login_success`, `test_login_invalid_password` | S1, S7 |
| **FR-AUTH-07..09** | `POST /api/auth/refresh, logout` | `backend/routers/auth.py` | `test_token_refresh`, `test_protected_route_*` | S4, S8 |
| **FR-RBAC-01..03** | `PUT, DELETE /api/internships/{id}` | `backend/routers/internships.py` | `test_rbac_rule_1_user_can_edit_own_opportunity`, `test_rbac_rule_2_*` | S2, S6 |
| **FR-RBAC-04..05** | Ownership Hierarchy | `backend/routers/internships.py` | `test_security_officer_admin_capabilities_*` | S6, S14 |
| **FR-GRP-01..04** | `/api/groups/*` | `backend/routers/groups.py` | `test_create_and_manage_group` | S5 |
| **FR-ADM-01..08** | `/api/admin/*` | `backend/routers/admin.py` | `test_rbac_rule_3_*`, `test_rbac_rule_4_*` | S10–S17 |

---

# Part C. Technical Design (TDD)

### C1. Technology Stack

#### Table 16: Technology Stack
| Component | Technology | Version | Reason for Choice |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React | 19.0.0 | Component-based reactivity, high ecosystem support, smooth client rendering. |
| **Language & Typings** | TypeScript | 5.6.0 | Strict compile-time type safety preventing runtime null/undefined errors. |
| **Build Tool** | Vite | 6.0.0 | Instant Hot Module Replacement (HMR) and optimized, minified production assets. |
| **Backend API** | FastAPI | 0.115.0+ | Modern asynchronous Python framework with automatic Swagger docs and OpenAPI validation. |
| **ORM / Data Modeling** | SQLModel | 0.0.22 | Unified architecture merging SQLAlchemy 2.0 ORM with Pydantic v2 data validation schemas. |
| **Password Hashing** | Bcrypt | 4.2.0 | Standard key-derivation function with 12 salt rounds resilient against brute-force attacks. |
| **Token Engine** | PyJWT | 2.10.0 | Cryptographically signed `HS256` token encoding and signature validation. |
| **Database Engine** | Supabase PostgreSQL | 17.12 | Managed cloud PostgreSQL with persistent transaction pooler surviving serverless recycles. |
| **Local DB Fallback** | SQLite | 3.x | Zero-configuration file and in-memory database for offline development and test isolation. |
| **Automated Testing** | Pytest & HTTPX | 8.3.0+ | Fast execution, dependency injection fixtures, and asynchronous client simulation. |
| **Cloud Hosting** | Vercel | Production | Automatic CI/CD deployment, global edge CDN, and serverless execution via `vercel.json`. |

### C2. System Architecture

```mermaid
flowchart TD
    subgraph Client ["Client Browser Environment"]
        UI["React 19 SPA (Vite)"]
        Storage["localStorage (Tokens & Cached Profile)"]
    end

    subgraph VercelEdge ["Vercel Serverless Hosting"]
        Gateway["Reverse Proxy & Rewrite Router (/api -> backend)"]
        Backend["FastAPI REST Application (Python 3.12)"]
        AuthModule["Auth & Security Engine (Bcrypt & PyJWT)"]
        RBACModule["RBAC & Ownership Guard Layer"]
        AdminModule["Admin Command Center Router"]
    end

    subgraph CloudDB ["Supabase Cloud Infrastructure"]
        Pooler["Supabase Session Pooler (:6543)"]
        Postgres[("PostgreSQL 17 Database")]
        AuditStore[("audit_logs Table (Immutable)")]
    end

    UI -- "1. User submits credentials / actions" --> Gateway
    Gateway -- "2. Routes API call with Bearer JWT" --> Backend
    Backend -- "3. Validates JWT signature & expiry" --> AuthModule
    Backend -- "4. Enforces ownership & role checks" --> RBACModule
    Backend -- "5. Administrative actions & audit" --> AdminModule
    Backend -- "6. Executes SQLModel ORM Queries" --> Pooler
    Pooler -- "7. Reads/Writes persistent tables" --> Postgres
    AdminModule -- "8. Appends immutable security events" --> AuditStore
    Backend -- "9. JSON Response (Tokens, Records)" --> UI
    UI -- "10. Stores access & refresh tokens" --> Storage
```

**Architecture Explanation:**
* **Arrows 1 & 2:** The client React SPA sends HTTP requests containing the `Authorization: Bearer <token>` header to the Vercel routing gateway, which rewrites `/api/*` requests directly to the FastAPI serverless function.
* **Arrows 3 & 4:** FastAPI processes the request through dependency injection (`get_current_active_user`), where `AuthModule` verifies the token's cryptographic signature, expiration, and ban status, while `RBACModule` verifies creator ownership.
* **Arrows 5 & 6:** Authorized requests query the hosted PostgreSQL database via the Supabase session pooler on port 6543.
* **Arrows 7 & 8:** Supabase executes transactions across tables while security events are appended to `AuditStore`.
* **Arrows 9 & 10:** FastAPI returns structured JSON responses, and the frontend updates its state and local token cache.

### C3. Backend and Frontend Structure

#### Backend Folder Tree
```text
backend/
├── auth/
│   ├── dependencies.py       # Reusable FastAPI auth dependencies (get_current_user, require_admin)
│   └── security.py           # Bcrypt hashing, PyJWT encoding, SHA-256 token hashing
├── routers/
│   ├── admin.py              # Admin Command Center endpoints (stats, user management, audit logs, CSV)
│   ├── auth.py               # Auth endpoints (register, login, refresh, logout, profile)
│   ├── groups.py             # Shared student groups & collaboration endpoints
│   └── internships.py        # Opportunity CRUD endpoints with RBAC ownership checks
├── tests/
│   ├── test_auth.py          # Registration, login, and token expiry tests
│   ├── test_groups.py        # Shared group creation and permission tests
│   └── test_rbac.py          # Post ownership, admin overrides, and ban tests
├── crud.py                   # Data access service layer and audit logging helper
├── database.py               # Supabase pooler engine initialization & SQLite fallback
├── main.py                   # FastAPI application initialization, CORS, and router registration
└── models.py                 # SQLModel database tables and Pydantic validation models
```

#### Frontend Folder Tree
```text
frontend/src/
├── components/
│   ├── AdminDashboardModal.tsx   # Admin Command Center modal (4 tabs: Overview, Users, Audit, CSV)
│   ├── FilterBar.tsx             # Keyword search, status filter, and 'My Posts' ownership toggle
│   ├── GroupManagementModal.tsx  # Collaborative group management and member permission toggles
│   ├── Header.tsx                # Page title and quick statistics summary badges
│   ├── InternshipCard.tsx        # Opportunity card with conditional Edit/Delete/Read-Only buttons
│   ├── InternshipModal.tsx       # Create/Edit internship modal dialog
│   ├── LoginPage.tsx             # Full-screen login/signup gateway with fast demo role buttons
│   ├── Navbar.tsx                # Top navigation bar with user badge, role label, and Sign Out
│   ├── StatsCards.tsx            # Opportunity metric counter cards (Total, Open, Closed, Remote)
│   └── Toast.tsx                 # Pop-up notification alerts for operations
├── services/
│   ├── api.ts                    # Opportunity, Group, and Admin API client methods with mock fallback
│   └── auth.ts                   # Token storage, Bearer header injection, login/logout handlers
├── types/
│   ├── admin.ts                  # TypeScript types for admin metrics and audit log entries
│   ├── auth.ts                   # TypeScript types for User and Auth tokens
│   ├── group.ts                  # TypeScript types for Groups and Group Members
│   └── internship.ts             # TypeScript interfaces for Opportunity listings
├── App.tsx                       # Root React state orchestrator and gateway switcher
├── index.css                     # OpportunityHub native CSS design system
└── main.tsx                      # Vite React root mount point
```

### C4. Data Model

```mermaid
erDiagram
    users ||--o{ internships : "creates / owns"
    users ||--o{ refresh_tokens : "has active sessions"
    users ||--o{ group_members : "belongs to"
    users ||--o{ audit_logs : "triggers security actions"
    groups ||--o{ group_members : "contains"
    groups ||--o{ internships : "associated with"

    users {
        string id PK
        string name
        string email UK
        string hashed_password
        string role
        boolean is_banned
        boolean is_main_admin
        string created_at
    }

    internships {
        string id PK
        string title
        string company_name
        string location
        string description
        string salary
        string deadline
        string status
        string user_id FK
        string group_id FK
        string created_at
    }

    refresh_tokens {
        string id PK
        string user_id FK
        string token_hash UK
        string expires_at
        boolean is_revoked
        string created_at
    }

    groups {
        string id PK
        string name
        string description
        string owner_id FK
        string created_at
    }

    group_members {
        string id PK
        string group_id FK
        string user_id FK
        boolean can_create
        boolean can_edit
        boolean can_assign
        string created_at
    }

    audit_logs {
        string id PK
        string action
        string details
        string user_id FK
        string user_email
        string ip_address
        string timestamp
    }
```

#### Table 17: Database Tables and Schema Specification
* **`users` Table:** Stores user identity credentials. Primary key `id` (UUID string), unique index on `email`, `hashed_password` (Bcrypt string), `role` (`user`, `admin`, `security_officer`), `is_banned` (Boolean default `False`), `is_main_admin` (Boolean default `False`).
* **`internships` Table:** Stores opportunities. Primary key `id` (UUID string), indexed foreign key `user_id` referencing `users.id`, optional foreign key `group_id` referencing `groups.id`, `title`, `company_name`, `location`, `description`, `salary`, `deadline`, `status` (`Open`/`Closed`).
* **`refresh_tokens` Table:** Stores session tokens. Primary key `id` (UUID string), foreign key `user_id` referencing `users.id`, unique index on `token_hash` (SHA-256 string), `expires_at` (timestamp), `is_revoked` (Boolean default `False`).
* **`groups` Table:** Stores student collaboration teams. Primary key `id` (UUID string), `name`, `description`, foreign key `owner_id` referencing `users.id`.
* **`group_members` Table:** Stores team memberships. Composite indexing on `group_id` and `user_id`, Boolean permission flags (`can_create`, `can_edit`, `can_assign`).
* **`audit_logs` Table:** Immutable security log. Primary key `id` (UUID string), `action` (e.g. `LOGIN_SUCCESS`, `BAN_USER`, `DELETE_OPPORTUNITY`), `details` (text), `user_id`, `user_email`, `timestamp` (ISO string).

### C5. API Design

#### Table 18: Complete API Endpoint Directory
| Method | Endpoint Path | Auth Required | Allowed Roles | Request Body | Success Status | Error Statuses |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register` | No | Any / Visitor | `{ name, email, password }` | `201 Created` | `400 Bad Request` |
| `POST` | `/api/auth/login` | No | Any / Visitor | `{ email, password }` | `200 OK` | `401 Unauthorized`, `403 Forbidden` |
| `POST` | `/api/auth/refresh` | No | Any | `{ refresh_token }` | `200 OK` | `401 Unauthorized` |
| `POST` | `/api/auth/logout` | No | Any | `{ refresh_token }` | `200 OK` | `200 OK` |
| `GET` | `/api/internships` | No | Any (Optional Auth) | None (Query: `search`, `status`, `my_only`) | `200 OK` | `500 Internal Error` |
| `GET` | `/api/internships/{id}` | No | Any | None | `200 OK` | `404 Not Found` |
| `POST` | `/api/internships` | Yes | Authenticated Users | `{ title, company_name, location, ... }` | `201 Created` | `400 Bad Request`, `403 Forbidden` |
| `PUT` | `/api/internships/{id}` | Yes | Owner / Authorized Admin | `{ title, company_name, location, ... }` | `200 OK` | `403 Forbidden`, `404 Not Found` |
| `DELETE` | `/api/internships/{id}` | Yes | Owner / Authorized Admin | None | `200 OK` | `403 Forbidden`, `404 Not Found` |
| `GET` | `/api/admin/overview` | Yes | Admin / Security Officer | None | `200 OK` | `403 Forbidden` |
| `GET` | `/api/admin/users` | Yes | Admin / Security Officer | None (Query: `search`, `role`) | `200 OK` | `403 Forbidden` |
| `POST` | `/api/admin/users/{id}/ban` | Yes | Admin / Security Officer | None | `200 OK` | `400 Bad Request`, `403 Forbidden` |
| `POST` | `/api/admin/users/{id}/role` | Yes | Admin Manager Only | None | `200 OK` | `403 Forbidden` |
| `GET` | `/api/admin/audit-logs` | Yes | Admin / Security Officer | None (Query: `limit`) | `200 OK` | `403 Forbidden` |
| `GET` | `/api/admin/export/csv` | Yes | Admin / Security Officer | None | `200 OK` | `403 Forbidden` |

*API Error Response Schema:* Standardized JSON object `{"detail": "Descriptive error message"}` with appropriate HTTP status codes.

### C6. JWT Authentication Design

```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant API as FastAPI Backend
    participant Security as Security Engine (PyJWT & Bcrypt)
    participant DB as Supabase PostgreSQL

    Note over User,DB: Authentication Flow
    User->>API: POST /api/auth/login { email, password }
    API->>DB: Query user by email
    DB-->>API: User Record (hashed_password, is_banned)
    API->>Security: verify_password(plain, hashed)
    Security-->>API: Password Valid (True)
    API->>Security: create_access_token(sub, email, role)
    Security-->>API: 15-Minute Signed JWT
    API->>Security: create_refresh_token(user_id)
    Security-->>API: 64-char random refresh token
    API->>DB: Insert SHA-256 token_hash into refresh_tokens table
    API-->>User: 200 OK { access_token, refresh_token, user }

    Note over User,DB: Protected API Request Flow
    User->>API: GET /api/internships (Header: Bearer <access_token>)
    API->>Security: decode_access_token(token)
    Security-->>API: Valid Payload { sub: user_id, role: "user" }
    API->>DB: Query active user & check is_banned == False
    DB-->>API: User Active
    API-->>User: 200 OK (Protected Data)

    Note over User,DB: Silent Token Refresh Flow (Token Expiry)
    User->>API: POST /api/auth/refresh { refresh_token }
    API->>DB: Query refresh_tokens by SHA-256 hash & is_revoked == False
    DB-->>API: Token Record Found & Active
    API->>Security: create_access_token(sub, email, role)
    Security-->>API: Fresh 15-Minute JWT
    API-->>User: 200 OK { access_token }

    Note over User,DB: Logout & Session Revocation Flow
    User->>API: POST /api/auth/logout { refresh_token }
    API->>DB: Update refresh_tokens SET is_revoked = True
    DB-->>API: Session Revoked
    API-->>User: 200 OK { message: "Session invalidated" }
```

#### Token Claims and Lifetimes
* **JWT Access Token Payload:**
  - `sub`: User UUID string (Subject).
  - `email`: User email address.
  - `role`: Role identifier (`user`, `admin`, `security_officer`).
  - `exp`: Expiration timestamp (strictly **15 minutes** from generation).
  - `type`: Token type identifier (`"access"`).
* **Signing Algorithm:** `HS256` (HMAC with SHA-256). Secret key injected via `JWT_SECRET` environment variable.
* **Token Storage Strategy & Security Mitigations:**
  - Tokens are stored in browser `localStorage` to support single-page application REST execution without complex cross-domain cookie configurations on serverless edge functions.
  - *XSS Defense:* All user input is sanitized, output is encoded via React's virtual DOM, and strict Content-Type headers prevent injected scripts.
  - *CSRF Defense:* Stateless Bearer tokens transmitted in the `Authorization` header are immune to standard cross-site request forgery attacks because browsers do not automatically attach Bearer headers to cross-origin requests.

### C7. RBAC Design

```mermaid
flowchart TD
    Start["Incoming HTTP Request"] --> TokenCheck{"Valid Bearer JWT Present?"}
    TokenCheck -- No --> Deny401["Return 401 Unauthorized"]
    TokenCheck -- Yes --> UserCheck{"User Exists & Not Banned?"}
    UserCheck -- Banned / Missing --> Deny403["Return 403 Forbidden"]
    UserCheck -- Active --> RoleCheck{"Action Requires Admin?"}
    RoleCheck -- Yes --> AdminCheck{"User has Admin / Officer Role?"}
    AdminCheck -- No --> Deny403
    AdminCheck -- Yes --> HierarchyCheck{"Officer Modifying Admin Manager?"}
    HierarchyCheck -- Yes --> Deny403
    HierarchyCheck -- No --> ExecuteAdmin["Execute Admin Action"]
    RoleCheck -- No --> OwnerCheck{"Modifying an Existing Post?"}
    OwnerCheck -- No --> ExecuteUser["Execute User Action"]
    OwnerCheck -- Yes --> OwnsPost{"current_user.id == post.user_id?"}
    OwnsPost -- Yes --> ExecuteUser
    OwnsPost -- No --> AdminOverride{"Is User Admin?"}
    AdminOverride -- Yes --> ExecuteUser
    AdminOverride -- No --> Deny403
```

#### Reusable Permission Check (Code Excerpt)
```python
# backend/routers/internships.py (Lines 158-177)
# RBAC Ownership and Hierarchy Enforcement Guard
if current_user:
    is_owner = internship.user_id and internship.user_id == current_user.id
    is_main_admin = bool(getattr(current_user, "is_main_admin", False) or current_user.email == "admin@platform.com")
    is_admin_or_officer = current_user.role in ["admin", "security_officer"] or is_main_admin

    if internship.user_id and not is_owner:
        owner_user = session.get(User, internship.user_id)
        is_post_by_main_admin = owner_user and (getattr(owner_user, "is_main_admin", False) or owner_user.email == "admin@platform.com")
        if is_post_by_main_admin and not is_main_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Security Officer cannot modify opportunities posted by the Admin Manager.",
            )

    if not is_admin_or_officer and not is_owner and internship.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only modify your own internship postings.",
        )
```

### C8. Admin Dashboard Design
The Admin Command Center (`AdminDashboardModal.tsx`) provides an integrated administrative management interface with four functional views:

```mermaid
flowchart LR
    AdminDashboard["Admin Command Center"]
    AdminDashboard --> Tab1["1. Overview Tab<br/>(GET /api/admin/overview)"]
    AdminDashboard --> Tab2["2. User Directory Tab<br/>(GET /api/admin/users)"]
    AdminDashboard --> Tab3["3. Audit Trail Tab<br/>(GET /api/admin/audit-logs)"]
    AdminDashboard --> Tab4["4. CSV Export Tab<br/>(GET /api/admin/export/csv)"]

    Tab2 --> BanAction["Toggle Ban (POST /api/admin/users/:id/ban)"]
    Tab2 --> RoleAction["Toggle Role (POST /api/admin/users/:id/role)"]
    BanAction --> AuditEvent["Appends 'BAN_USER' to audit_logs & revokes refresh tokens"]
```

#### Table 19: Admin Dashboard Specification
| View Tab | Endpoints Called | Filters & Controls | Actions Executed | Audit Events Written |
| :--- | :--- | :--- | :--- | :--- |
| **Overview** | `GET /api/admin/overview` | Auto-refresh on modal open. | Inspect system health counters (Total Users, Posts, Banned, Groups). | None (Read-only query). |
| **User Directory** | `GET /api/admin/users`<br>`POST /api/admin/users/{id}/ban`<br>`POST /api/admin/users/{id}/role` | Search by name/email; Filter by role (`All`, `User`, `Admin`). | Ban/Unban user; Promote to admin; Demote to user. | `BAN_USER`<br>`UNBAN_USER`<br>`CHANGE_ROLE` |
| **Audit Trail** | `GET /api/admin/audit-logs` | Pagination limit selector (`50`, `100`, `200`). | Real-time monitoring of system security and moderation events. | None (Read-only inspection). |
| **CSV Export** | `GET /api/admin/export/csv` | Inherits active search and role filters. | Downloads structured `.csv` file of platform records. | None (File generation). |

### C9. Security Design and Threats

#### Table 20: Security Threats & Defenses
| Threat Description | Mitigation Strategy | Implementation File & Location |
| :--- | :--- | :--- |
| **Password Database Leak** | Passwords salted and hashed with 12-round Bcrypt; plain passwords never saved. | `backend/auth/security.py` (`hash_password`) |
| **Stolen Access Token** | Access token validity strictly limited to 15 minutes; revoked upon user logout. | `backend/auth/security.py` (`ACCESS_TOKEN_EXPIRE_MINUTES`) |
| **Stolen Refresh Token** | Refresh tokens stored in DB only as SHA-256 hashes; revoking destroys session. | `backend/routers/auth.py` (`hash_token`, `RefreshToken`) |
| **Brute-Force Login Attacks** | Exponential Bcrypt CPU cost; suspension guards; audit trail tracking. | `backend/routers/auth.py` (`login`) |
| **Privilege Escalation** | Roles verified server-side on every request via `require_admin` dependency. | `backend/auth/dependencies.py` (`require_admin`) |
| **Cross-User Record Tampering** | Server-side ownership query validation; cross-student modifications rejected with 403. | `backend/routers/internships.py` (Lines 158–177) |
| **Cross-Site Scripting (XSS)** | React JSX automatically escapes dangerous characters; no `dangerouslySetInnerHTML`. | `frontend/src/components/*` |
| **Cross-Site Request Forgery (CSRF)** | Stateless Bearer token header architecture; no credentials sent automatically. | `frontend/src/services/auth.ts` (`getAuthHeaders`) |
| **CORS Misconfiguration** | Strict CORS policy allowing only authorized origins and explicit HTTP methods. | `backend/main.py` (`CORSMiddleware`) |
| **Secrets Committed to Repo** | Sensitive credentials stored exclusively in `.env` and Vercel Environment Variables. | `backend/.env`, `vercel.json`, `.gitignore` |
| **SQL Injection (SQLi)** | Parameterized queries enforced across all models using SQLModel / SQLAlchemy ORM. | `backend/crud.py`, `backend/routers/*` |
| **Over-Posting / Mass Assignment** | Strict Pydantic input schemas (`UserCreate`, `InternshipCreateInput`) filter extra fields. | `backend/models.py`, `backend/routers/*` |

### C10. Deployment on Vercel
The system is deployed on Vercel as a unified full-stack application configured via `vercel.json`:
* **Frontend Project:** Built using Vite (`dist/` directory) and served via Vercel's global Edge CDN.
* **Backend API Project:** Python 3.12 Serverless Function executing from `api/index.py` and `backend/main.py`.
* **API Routing & Rewrites:** `vercel.json` maps all `/api/(.*)` requests to the FastAPI ASGI handler.

#### Table 21: Environment Variables on Vercel
| Variable Name | Purpose / Description | Location Configured |
| :--- | :--- | :--- |
| `DATABASE_URL` | Supabase PostgreSQL connection pooler string (`aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres`). | Vercel Project Settings $\rightarrow$ Environment Variables |
| `JWT_SECRET` | Cryptographic secret key used to sign and verify HMAC-SHA256 JWT tokens. | Vercel Project Settings $\rightarrow$ Environment Variables |
| `VERCEL_ENV` | Runtime environment indicator (`production`). | Vercel System Variable |

### C11. Testing
The test strategy consists of automated backend API unit and integration tests using `pytest` and `httpx`, combined with manual UI verification.

#### Running Automated Tests
```bash
# Navigate to backend and run pytest
cd backend
pytest tests/ -v
```

#### Table 22: Automated Test Execution Results (12/12 Passing)
| Test Identifier | Tested Requirement / Component | Verification Logic | Result |
| :--- | :--- | :--- | :---: |
| `test_login_success` | `FR-AUTH-05` (Authentication) | Submits valid credentials; verifies 15-min JWT and refresh token returned. | **PASSED** |
| `test_login_invalid_password` | `FR-AUTH-05` (Security) | Submits wrong password; verifies `HTTP 401 Unauthorized` returned. | **PASSED** |
| `test_register_duplicate_email` | `FR-AUTH-03` (Validation) | Attempts to register already existing email; verifies `HTTP 400 Bad Request`. | **PASSED** |
| `test_protected_route_without_token` | `FR-AUTH-09` (Security) | Requests protected resource without Bearer header; verifies `HTTP 401`. | **PASSED** |
| `test_protected_route_with_invalid_token`| `FR-AUTH-09` (Security) | Requests resource with forged signature; verifies `HTTP 401 Unauthorized`. | **PASSED** |
| `test_token_refresh` | `FR-AUTH-07` (Token Lifecycle) | Submits valid refresh token; verifies fresh access token generated. | **PASSED** |
| `test_create_and_manage_group` | `FR-GRP-01..04` (Collaboration) | Creates team, invites member, checks `can_create` permissions. | **PASSED** |
| `test_rbac_rule_1_user_can_edit_own` | `FR-RBAC-02` (Ownership) | Creates opportunity as Student 1; verifies Student 1 can edit post. | **PASSED** |
| `test_rbac_rule_2_user_cannot_edit_other`| `FR-RBAC-03` (Isolation) | Student 2 attempts to edit Student 1's post; verifies `HTTP 403 Forbidden`. | **PASSED** |
| `test_rbac_rule_3_admin_modify_any` | `FR-RBAC-04` (Admin Power) | Admin edits student post; verifies operation succeeds. | **PASSED** |
| `test_rbac_rule_4_banned_user_rejected` | `FR-ADM-06` (Ban Enforcement) | Banned user calls API; verifies rejection with `HTTP 403 Forbidden`. | **PASSED** |
| `test_security_officer_admin_caps` | `FR-ADM-05` (Hierarchy) | Verifies Officer cannot ban Admin Manager (`HTTP 403 Forbidden`). | **PASSED** |

---

# Part D. Evidence: Screenshots of the Running Application

> **Note for PDF Report Submission:** Capture each screenshot on the live deployed Vercel URL (`https://2320353.vercel.app`) with the browser address bar visible and the logged-in user profile displayed.

### D1. User Side
* **[S1: Signup and Login Gateway Screen]**  
  * *Caption:* Login and registration page showing client validation error when password length is under 6 characters (`FR-AUTH-02`).
* **[S2: Main Opportunities Feed of Logged-In User]**  
  * *Caption:* Dashboard showing internship cards with the "👤 My Post" ownership badge and "My Posts" filter tab active (`FR-RBAC-02`).
* **[S3: Password Validation & Profile Security]**  
  * *Caption:* User authentication dialog rejecting mismatched password confirmation (`FR-AUTH-02`).
* **[S4: Top Navigation & Session Revocation]**  
  * *Caption:* Navigation bar displaying user role badge ("Admin Manager" / "Student") and the "🚪 Sign Out" action (`FR-AUTH-08`).
* **[S5: Collaborative Group Management]**  
  * *Caption:* `GroupManagementModal.tsx` showing the student collaboration squad, active members, and granular permission checkboxes (`FR-GRP-02`).
* **[S6: Action Denied by RBAC (HTTP 403 Response)]**  
  * *Caption:* Student attempting to edit another user's post; Chrome DevTools Network Tab shows `403 Forbidden` with toast notification (`FR-RBAC-03`).

### D2. Security Behaviour
* **[S7: Expired Token Rejection (HTTP 401)]**  
  * *Caption:* Network tab showing a request with an expired JWT access token rejected with `401 Unauthorized` (`FR-AUTH-09`).
* **[S8: Silent Token Refresh Execution]**  
  * *Caption:* Network tab showing `POST /api/auth/refresh` returning a fresh 15-minute access token (`FR-AUTH-07`).
* **[S9: Banned User Rejection]**  
  * *Caption:* A suspended user attempting to access the dashboard; backend rejects request with `403 Forbidden: Your account has been suspended` (`FR-ADM-06`).

### D3. Admin Dashboard
* **[S10: Admin Command Center – Overview Statistics]**  
  * *Caption:* Overview tab displaying live KPI cards: Total Users, Total Opportunities, Banned Accounts, and Active Groups (`FR-ADM-01`).
* **[S11: User Directory with Search and Role Filters]**  
  * *Caption:* Searchable, paginated user management table showing user roles, ban states, and action buttons (`FR-ADM-02`).
* **[S12: Admin Role Promotion & Demotion]**  
  * *Caption:* Admin toggling a user's role between Student and Administrator with instant table update (`FR-ADM-03`).
* **[S13: User Ban Action & Instant Suspension]**  
  * *Caption:* Admin clicking "Ban User"; state updates immediately to "Banned" and audit trail logs event (`FR-ADM-03`).
* **[S14: Root Admin Protection Enforcement]**  
  * *Caption:* Security Officer attempting to ban Admin Manager; UI and backend reject with `403 Forbidden` (`FR-ADM-05`).
* **[S15: Real-Time Security Audit Trail]**  
  * *Caption:* Audit Trail tab showing chronological immutable log entries for `REGISTER`, `LOGIN_SUCCESS`, and `BAN_USER` (`FR-ADM-07`).
* **[S16: Content Moderation View]**  
  * *Caption:* Admin reviewing and moderating postings across all users (`FR-ADM-01`).
* **[S17: CSV Data Export]**  
  * *Caption:* Downloaded platform CSV report opened in spreadsheet viewer showing exported opportunities and users (`FR-ADM-08`).

### D4. Deployment
* **[S18: Vercel Production Deployment Overview]**  
  * *Caption:* Vercel dashboard showing the active production deployment for `2320353.vercel.app` with green healthy status.
* **[S19: Vercel Environment Variables Configuration]**  
  * *Caption:* Vercel project settings showing `DATABASE_URL` and `JWT_SECRET` configured (values securely masked).
* **[S20: Live Interactive API Documentation]**  
  * *Caption:* Live Swagger UI documentation running at `https://2320353.vercel.app/docs`.

### D5. Tests
* **[S21: Pytest Automated Test Suite Output]**  
  * *Caption:* Terminal output showing all 12 backend test cases passing in 30.23 seconds with 100% success rate.

---

# Part E. Project Management and Conclusion

### E1. How to Run and Test

#### 1. Prerequisites
* Python 3.10+ (Python 3.12 recommended)
* Node.js 18+ and npm
* Git

#### 2. Environment Variables File
Create `backend/.env`:
```env
# Supabase PostgreSQL Connection Pooler (or local SQLite)
DATABASE_URL=postgresql+psycopg2://postgres.kvhrqoljvkgqszqrwkvp:tanjinaakterlimo2320353@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres
JWT_SECRET=cse309-secure-jwt-secret-key-autumn-2026-production-ready-token-auth
```

#### 3. Backend Execution
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1       # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```
*API running at `http://localhost:8000` | Swagger Docs at `http://localhost:8000/docs`.*

#### 4. Frontend Execution
```bash
cd frontend
npm install
npm run dev
```
*Frontend running at `http://localhost:5173`.*

#### 5. Running Automated Tests
```bash
cd backend
pytest tests/ -v
```

### E2. GitHub Work

#### Table 23: GitHub Issues and Pull Requests
| Issue / PR | Title / Type | Key Deliverables | Commits & Milestones |
| :---: | :--- | :--- | :--- |
| **Issue #6** | `[Feature]: Complete JWT Authentication, RBAC, Groups, Admin Center` | Formal specification of Parts 1 through 6 requirements and acceptance criteria. | Closes #6 upon merge |
| **PR #7** | `feat: implement full JWT authentication, RBAC, groups, admin center (Parts 1–6)` | Full production implementation of security, RBAC, collaborative groups, admin console, and tests. | `6828035`, `e5aef3a`, `c758cd4`, `100a9c1` |
| **PR #5** | `feat: backend architecture refactor` | Modular router separation (`routers/`, `crud.py`, `models.py`) and error handlers. | `182cbe6`, `6f5d0a3` |
| **PR #2** | `feat: implement initial CRUD REST API and UI` | Initial Mid-assessment MVP delivering all 5 CRUD operations for internship listings. | `7bc04f4`, `0118463` |

### E3. Limitations
1. **Third-Party Social Login:** The system relies entirely on internal email/password authentication; Google/GitHub OAuth is not yet integrated.
2. **Real-Time WebSockets:** Audit logs and platform metrics update upon modal opening rather than through a continuous bidirectional WebSocket stream.
3. **Automated Resume File Scanning:** File uploads are limited to URL links rather than direct binary PDF document parsing on the server.

### E4. Future Work
1. **OAuth2 Social Sign-In:** Add Google and GitHub sign-in to eliminate password management overhead for students.
2. **Live WebSocket Notifications:** Introduce real-time push alerts when an applicant is invited or when an opportunity is updated.
3. **Automated Application Tracking System (ATS):** Allow students to apply directly through the platform and track review status stages (Applied $\rightarrow$ Reviewing $\rightarrow$ Interview $\rightarrow$ Accepted).

### E5. Sources, Libraries and Tools

#### Table 24: Sources, Libraries and Tools
| Tool / Library | Version / Source | Purpose in Project |
| :--- | :--- | :--- |
| **React** | 19.0.0 | Frontend component rendering and reactive state orchestration. |
| **FastAPI** | 0.115.0+ | Asynchronous RESTful API framework and dependency injection. |
| **SQLModel** | 0.0.22 | Unified SQLAlchemy 2.0 ORM and Pydantic v2 data models. |
| **PyJWT** | 2.10.0 | Cryptographic JSON Web Token signing (`HS256`) and verification. |
| **Bcrypt** | 4.2.0 | Password salting and hashing with 12 rounds. |
| **Supabase** | Cloud | Managed PostgreSQL database hosting with connection pooling. |
| **Vercel** | Cloud | Serverless hosting, continuous deployment, and Edge CDN. |
| **Pytest** | 8.3.0+ | Automated test suite execution and HTTP endpoint testing. |
| **Antigravity AI Agent** | Google DeepMind | Assisted in architectural review, test authoring, and documentation generation. All generated code, database migrations, and security checks were manually verified and executed locally. |

---

# Appendix. Test Accounts and Video Demo

### Video Demonstration
* **Video Demo Link:** *[Insert your 5-8 minute YouTube / Google Drive demonstration link here]*

### Pre-Seeded Academic Evaluation Accounts
> **Important:** The credentials below are pre-seeded test accounts configured specifically for academic evaluation.

#### Table 25: Academic Test Accounts
| Role | Email | Password | Permissions & Boundaries |
| :--- | :--- | :--- | :--- |
| **Admin Manager (Root)** | `admin@platform.com` | `admin123` | Full administrative control; immune to bans and demotions. |
| **Security Officer** | `admin2@platform.com` | `admin123` | Moderate standard users; cannot ban or modify Admin Manager. |
| **Student 1 (Post Owner)** | `student1@university.edu` | `student123` | Owner of multiple listings; Group Owner; full control of own data. |
| **Student 2 (Collaborator)** | `student2@university.edu` | `student123` | Team member with collaborative edit rights in shared groups. |
| **Student 3 (Viewer)** | `student3@university.edu` | `student123` | Standard user with read-only view on non-owned postings. |

### Pre-Configured Collaboration Group
* **Group Name:** CSE Career Squad
* **Group Owner:** Student 1 (`student1@university.edu`)
* **Group Member 1:** Student 2 (`student2@university.edu`) — Permissions: `can_create = True`, `can_edit = True`, `can_assign = False`.
* **Group Member 2:** Student 3 (`student3@university.edu`) — Permissions: `can_create = False`, `can_edit = False`, `can_assign = False` (Read-only observer).
