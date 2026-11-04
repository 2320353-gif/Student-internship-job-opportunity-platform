@echo off
cd /d "%~dp0"
echo ========================================================
echo Starting FastAPI Backend on Port 8000...
echo ========================================================
".venv\Scripts\fastapi.exe" dev main.py
pause
