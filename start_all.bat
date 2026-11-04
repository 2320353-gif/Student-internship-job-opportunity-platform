@echo off
cd /d "%~dp0"
echo ========================================================
echo Launching Backend and Frontend for CSE309 MVP Assessment
echo ========================================================

start "FastAPI Backend (Port 8000)" cmd /k "run_backend.bat"
start "React Frontend (Port 5173)" cmd /k "run_frontend.bat"

echo Backend URL: http://localhost:8000/docs
echo Frontend URL: http://localhost:5173
pause
