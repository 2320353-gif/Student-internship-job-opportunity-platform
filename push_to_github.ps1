$env:Path = "C:\Program Files\Git\cmd;" + $env:Path
Set-Location $PSScriptRoot
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Pushing project to GitHub repository..." -ForegroundColor Green
Write-Host "Repo: https://github.com/2320353-gif/Student-internship-job-opportunity-platform.git" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

Write-Host "Pushing 'main' branch..." -ForegroundColor Green
git push -u origin main

Write-Host "Pushing 'feature/internship-crud' branch..." -ForegroundColor Green
git push -u origin feature/internship-crud

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Done! Check your GitHub repository." -ForegroundColor Green
