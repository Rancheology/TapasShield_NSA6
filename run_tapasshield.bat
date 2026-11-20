@echo off
title TapasShield IIoT Platform (NSA 6.0) - Shared Online Register
echo ======================================================================
echo   TapasShield (NSA 6.0) - Industrial IIoT Boiler Platform
echo   Shared Secure Online Register: Business + State + Central Govt
echo ======================================================================
echo.
echo [1/2] Launching TapasShield Backend & Static Web Cockpit on port 8000...
start "" http://localhost:8000
echo [2/2] Starting Uvicorn Server with Live SIL Digital Twin...
echo Server running at: http://localhost:8000
echo Press Ctrl+C in this window to stop the server.
echo.
conda run -n tapasshield-nsa6 uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause

