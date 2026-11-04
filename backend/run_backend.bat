@echo off
cd /d "%~dp0"
echo ========================================================
echo Starting FastAPI Backend (Student Internship Platform)
echo ========================================================
if exist ".venv\Scripts\fastapi.exe" (
    ".venv\Scripts\fastapi.exe" dev main.py
) else if exist ".venv\Scripts\uvicorn.exe" (
    ".venv\Scripts\uvicorn.exe" main:app --reload --port 8000
) else (
    echo [ERROR] Virtual environment not found. Please run:
    echo python -m venv .venv
    echo .venv\Scripts\pip install -r requirements.txt
)
pause
