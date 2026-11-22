@echo off
title FreshWatch - Launching Servers
echo ===================================================
echo Starting FreshWatch Supermarket Intelligence System
echo ===================================================

echo [1/2] Starting Python FastAPI ML Microservice on port 8000...
start "FreshWatch ML Service" cmd /k "cd /d C:\Users\LENOVO\Desktop\expiry_project && C:\Users\LENOVO\AppData\Local\Programs\Python\Python313\python.exe -m uvicorn ml_service.main:app --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Next.js Web Application on port 3000...
start "FreshWatch Web App" cmd /k "cd /d C:\Users\LENOVO\Desktop\expiry_project && npm.cmd run start"

timeout /t 3 /nobreak >nul

echo Opening FreshWatch in your default browser...
start http://localhost:3000

echo All systems running!
exit
