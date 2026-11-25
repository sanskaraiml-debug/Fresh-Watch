@echo off
title Inventory Analysis - Launching Servers
echo ===================================================
echo Starting Inventory Analysis Supermarket System
echo ===================================================

echo [1/2] Starting Python FastAPI ML Microservice on port 8000...
start "Inventory Analysis ML Service" cmd /k "cd /d C:\Users\LENOVO\Desktop\expiry_project && C:\Users\LENOVO\AppData\Local\Programs\Python\Python313\python.exe -m uvicorn ml_service.main:app --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Next.js Web Application on port 3000...
start "Inventory Analysis Web App" cmd /k "cd /d C:\Users\LENOVO\Desktop\expiry_project && npm.cmd run start"

timeout /t 3 /nobreak >nul

echo Opening Inventory Analysis in your default browser...
start http://localhost:3000

echo All systems running!
exit
