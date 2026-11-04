$nodeDir = "C:\Users\AFRIN\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64"
$env:Path = "$nodeDir;$env:Path"
Set-Location (Join-Path $PSScriptRoot "frontend")
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting Vite/React Frontend on http://localhost:5173" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
npm run dev
