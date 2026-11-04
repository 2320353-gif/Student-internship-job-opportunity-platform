@echo off
cd /d "%~dp0"
set "PATH=C:\Program Files\Git\cmd;%PATH%"
echo ========================================================
echo Pushing project to GitHub...
echo Repository: https://github.com/2320353-gif/Student-internship-job-opportunity-platform.git
echo ========================================================
echo.
echo Pushing branch 'main'...
git push -u origin main
echo.
echo Pushing branch 'feature/internship-crud'...
git push -u origin feature/internship-crud
echo.
echo ========================================================
echo Project successfully pushed to GitHub!
echo ========================================================
pause
