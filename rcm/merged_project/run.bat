@echo off
echo Starting RCM - Code Visualizer & Diagram Generator
echo.

cd /d %~dp0

echo Starting Backend Server...
start "RCM Backend" cmd /k "cd /d %~dp0backend && python app.py"

timeout /t 2 /nobreak >nul

echo Starting Frontend...
start "RCM Frontend" cmd /k "cd /d %~dp0frontend && streamlit run app.py"

echo.
echo RCM is starting!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8501
echo.
pause
