$pythonDir = "C:\Users\AFRIN\AppData\Local\Programs\Python\Python312"
$env:Path = "$pythonDir;$pythonDir\Scripts;$env:Path"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting FastAPI Backend on http://localhost:8000" -ForegroundColor Green
Write-Host "Docs available at http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
& (Join-Path $PSScriptRoot ".venv\Scripts\fastapi.exe") dev main.py
