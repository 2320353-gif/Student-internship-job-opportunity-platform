# 🎓 CSE309 Mid Project Assessment – Viva & Demo Complete Guide (30/30 Marks)

**Course:** CSE309 Web Engineering / Advanced Web Development  
**Project Name:** `Student-internship-job-opportunity-platform`  
**Feature (MVP):** Internship Opportunity Manager  
**Tech Stack:** React + TypeScript + Vite (Frontend) | FastAPI + Python + SQLModel (Backend) | SQLite / Supabase PostgreSQL (Database)

---

## 📋 Marks Breakdown (Total: 30 Marks)
* **Frontend Implementation (10 Marks):** Complete React + TypeScript UI with all 5 CRUD actions, responsive design, stats aggregation, search, and validation.
* **Backend Implementation (10 Marks):** Robust FastAPI REST API with endpoints for all 5 CRUD operations, proper HTTP status codes (`201`, `200`, `404`, `422`), CORS, and database integration.
* **GitHub Presentation + Viva (10 Marks):** Ability to demonstrate CRUD in the UI, trace Network requests in DevTools, explain endpoints in Swagger `/docs`, test with Postman, and explain the database schema.

---

## 🚀 How to Run the Project Locally

### 1. Start the Backend (Terminal 1)
```powershell
cd C:\Users\AFRIN\OneDrive\Desktop\CSE309MID\Student-internship-job-opportunity-platform\backend

# Option A: With virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py

# Option B: Run directly with uvicorn
uvicorn main:app --reload --port 8000
```
> Backend runs at: **`http://localhost:8000`**  
> Interactive Swagger API Documentation: **`http://localhost:8000/docs`**

### 2. Start the Frontend (Terminal 2)
```powershell
cd C:\Users\AFRIN\OneDrive\Desktop\CSE309MID\Student-internship-job-opportunity-platform\frontend
npm install
npm run dev
```
> Frontend runs at: **`http://localhost:5173`** (Automatically proxies `/api/*` to `http://localhost:8000`)

---

## 🎯 The 5 Viva Demonstration Points (Step-by-Step)

### Item 1: CRUD Operations Demo in Frontend (10 Marks)
| Operation | Action in UI | Behind the Scenes |
|---|---|---|
| **1. Create** | Click **"+ Post Internship"** top button -> Fill out form -> Click **"Publish Opportunity"** | Sends `POST /api/internships` with JSON body. Backend validates with Pydantic, generates UUID, saves to DB, returns `201 Created`. |
| **2. Read List** | View cards on homepage, use search bar or status tabs (**All / Open / Closed**) | Sends `GET /api/internships?search=...&status=...`. Returns list of matching records. |
| **3. Read Single** | Click **"👁 View Details"** on any card | Sends `GET /api/internships/{id}`. Displays modal with complete description, metadata, deadline, and UUID. |
| **4. Update** | Click **"✏️ Edit"** on any card -> Modify fields -> Click **"Save Changes"** | Sends `PUT /api/internships/{id}` with updated fields. Backend updates DB, returns `200 OK`. |
| **5. Delete** | Click **"🗑 Delete"** on any card -> Confirm in popup | Sends `DELETE /api/internships/{id}`. Backend deletes record from DB and returns `200 OK`. |

---

### Item 2: Request Flow in Browser Developer Tools
**How to show the examiner:**
1. Open Chrome or Edge Developer Tools (**Press F12** or right-click -> Inspect).
2. Go to the **Network** tab.
3. Check the **Fetch/XHR** filter.
4. Perform any action (e.g. click "Post Internship" or "Edit"):
   - **Show Headers:** Request URL (`http://localhost:5173/api/internships`), Request Method (`POST` / `PUT` / `DELETE`), Status Code (`201 Created` or `200 OK`).
   - **Show Request Payload:** Show JSON body containing `title`, `company_name`, `location`, `salary`, `deadline`, etc.
   - **Show Response:** Show the JSON returned by FastAPI with the assigned `id` and `created_at`.

---

### Item 3: REST API Explanation
All endpoints are available in Swagger UI at: **`http://localhost:8000/docs`**

| Method | Endpoint | Description | Request Body | Status Code |
|---|---|---|---|---|
| `POST` | `/api/internships` | Create new internship | `InternshipCreate` JSON | `201 Created` |
| `GET` | `/api/internships` | Read all internships (with search/filter) | None (Query params) | `200 OK` |
| `GET` | `/api/internships/{id}` | Read single internship details | None | `200 OK` (or `404`) |
| `PUT` | `/api/internships/{id}` | Update existing internship | `InternshipUpdate` JSON | `200 OK` (or `404`) |
| `DELETE` | `/api/internships/{id}` | Delete internship | None | `200 OK` (or `404`) |
| `GET` | `/api/internships/stats/summary` | Get aggregated dashboard counts | None | `200 OK` |
| `GET` | `/api/health` | Health check endpoint | None | `200 OK` |

---

### Item 4: Postman API Testing
If the instructor asks you to test the API with Postman or cURL, use these requests:

#### 1. Create Internship (POST)
```bash
curl -X POST "http://localhost:8000/api/internships" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning Intern",
    "company_name": "DataGen AI",
    "location": "Dhaka, Bangladesh",
    "description": "Develop prompt pipelines and computer vision algorithms.",
    "salary": "৳16,000 / month",
    "deadline": "2026-12-20",
    "status": "Open"
  }'
```

#### 2. Get All Internships (GET)
```bash
curl -X GET "http://localhost:8000/api/internships"
```

#### 3. Get Single Internship (GET with ID)
```bash
curl -X GET "http://localhost:8000/api/internships/{REPLACE_WITH_UUID}"
```

#### 4. Update Internship (PUT)
```bash
curl -X PUT "http://localhost:8000/api/internships/{REPLACE_WITH_UUID}" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": "৳20,000 / month",
    "status": "Closed"
  }'
```

#### 5. Delete Internship (DELETE)
```bash
curl -X DELETE "http://localhost:8000/api/internships/{REPLACE_WITH_UUID}"
```

---

### Item 5: Database Schema Explanation
Explain the `internships` table structure:
```sql
CREATE TABLE internships (
    id VARCHAR PRIMARY KEY,               -- Unique UUID string
    title VARCHAR NOT NULL,               -- Internship title
    company_name VARCHAR NOT NULL,        -- Company name
    location VARCHAR NOT NULL,            -- Location / Remote
    description TEXT NOT NULL,            -- Job responsibilities
    salary VARCHAR DEFAULT 'Unpaid',      -- Compensation
    deadline VARCHAR NOT NULL,            -- Deadline (YYYY-MM-DD)
    status VARCHAR DEFAULT 'Open',        -- Open or Closed
    created_at VARCHAR                    -- Timestamp
);
```

#### Supabase Integration (Optional/Cloud Setup):
- Local database uses SQLite (`internships.db`) managed via **SQLModel**.
- To connect to **Supabase**, simply set `DATABASE_URL` in `backend/.env` with your Supabase PostgreSQL connection string. SQLModel will automatically migrate and create the table on startup!

---

## 💡 Quick Viva Q&A Cheat Sheet

1. **Q: Why did you use SQLModel instead of raw SQL or pure SQLAlchemy?**  
   *A:* SQLModel was created by the author of FastAPI (Sebastián Ramírez). It unifies Pydantic schemas and SQLAlchemy models into a single class, avoiding code duplication for data validation and database persistence.

2. **Q: How does the React frontend communicate with FastAPI?**  
   *A:* In development, the Vite dev server forwards requests starting with `/api` to `http://localhost:8000` via the proxy defined in `vite.config.ts`. In production on Vercel, `vercel.json` rewrites `/api/*` to the FastAPI backend service.

3. **Q: How are errors handled (e.g. 404 or 422)?**  
   *A:* FastAPI automatically validates request schemas with Pydantic and returns `422 Unprocessable Entity` if required fields are missing. If an invalid UUID is passed to `GET /api/internships/{id}`, FastAPI raises an `HTTPException(status_code=404, detail="Internship not found")`.
