@echo off
cd /d "%~dp0"
set "PATH=C:\Users\AFRIN\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
echo ========================================================
echo Starting Vite/React Frontend on port 5173
echo ========================================================
call npm.cmd run dev
pause
