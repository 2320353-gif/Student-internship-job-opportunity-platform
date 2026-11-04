# Student Internship & Job Opportunity Platform
### CSE309 Mid Project Assessment – MVP (Internship Opportunity Manager)

A full-stack web application built for **CSE309 Autumn 2026 Mid Project Assessment**, featuring an **Internship Opportunity Manager** that implements all 5 CRUD operations across both the React + TypeScript frontend and FastAPI Python backend.

---

## 🛠️ Tech Stack

- **Frontend:** React 19, TypeScript, Vite, Modern CSS (Responsive Design)
- **Backend:** Python 3.10+, FastAPI, SQLModel (SQLAlchemy + Pydantic)
- **Database:** SQLite (local zero-config) / Supabase (PostgreSQL ready)
- **Deployment:** Vercel configured via `vercel.json`

---

## 🚀 Getting Started

### 1. Run Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1       # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```
> The API will start at `http://localhost:8000`.  
> Interactive API Swagger Documentation is available at: `http://localhost:8000/docs`.

### 2. Run Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
> The web application will start at `http://localhost:5173`.  
> Requests sent to `/api` are automatically proxied to the FastAPI server at `http://localhost:8000`.

---

## 📋 Implemented CRUD Operations

| Operation | Frontend UI Action | HTTP Method & Endpoint |
|---|---|---|
| **Create** | Click "+ Post Internship" button and submit form | `POST /api/internships` |
| **Read List** | Browse cards, search by keyword, or filter by status | `GET /api/internships` |
| **Read Single** | Click "View Details" on any internship card | `GET /api/internships/{id}` |
| **Update** | Click "Edit" on any card and submit updated fields | `PUT /api/internships/{id}` |
| **Delete** | Click "Delete" on any card and confirm removal | `DELETE /api/internships/{id}` |

---

## 📂 Project Structure

```
Student-internship-job-opportunity-platform/
├── backend/
│   ├── database.py         # DB connection (SQLite / Supabase) and initial seed data
│   ├── models.py           # SQLModel table definitions and Pydantic schemas
│   ├── main.py             # FastAPI application with all 5 CRUD endpoints & CORS
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/     # Navbar, StatsCards, FilterBar, InternshipCard, Modals, Toast
│   │   ├── services/       # API client for backend communication with fallback
│   │   ├── types/          # TypeScript interfaces for Internship data
│   │   ├── App.tsx         # Main application orchestrator
│   │   ├── index.css       # Clean, modern, responsive styling
│   │   └── main.tsx        # React root entrypoint
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts      # Vite dev server with /api proxy
├── VIVA_DEMO_GUIDE.md      # Comprehensive step-by-step viva & demo guide
├── vercel.json             # Vercel deployment configuration
└── README.md
```

---

## 🎓 Viva & Demo Guide
For complete step-by-step instructions on demonstrating the 5 required features during your viva assessment (DevTools request flow, Swagger `/docs`, Postman requests, and database schema), see [`VIVA_DEMO_GUIDE.md`](./VIVA_DEMO_GUIDE.md).
