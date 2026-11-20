# TapasShield IIoT Platform (NSA 6.0) - One-Click PowerShell Launcher
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  TapasShield (NSA 6.0) - Industrial IIoT Boiler Platform" -ForegroundColor Green
Write-Host "  Shared Secure Online Register: Business + State + Central Govt" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Opening browser to http://localhost:8000..." -ForegroundColor Gray
Start-Process "http://localhost:8000"
Write-Host "[2/2] Starting Uvicorn Server with Live SIL Digital Twin..." -ForegroundColor Green
Write-Host "Server running at: http://localhost:8000" -ForegroundColor White
Write-Host "Press Ctrl+C to terminate server." -ForegroundColor Yellow
Write-Host ""
conda run -n tapasshield-nsa6 uvicorn backend.main:app --host 0.0.0.0 --port 8000

