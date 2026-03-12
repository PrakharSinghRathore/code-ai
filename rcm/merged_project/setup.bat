@echo off
echo Setting up RCM - Code Visualizer & Diagram Generator
echo.

cd /d %~dp0

echo.
echo === Installing Backend Dependencies ===
cd backend
python -m pip install flask flask-cors python-dotenv requests

echo.
echo === Installing Frontend Dependencies ===
cd ..\frontend
python -m pip install streamlit requests

echo.
echo === Setup Complete ===
echo.
echo To run the project:
echo   run.bat
echo.
echo Or manually:
echo   - Backend: cd backend ^&^& python app.py
echo   - Frontend: cd frontend ^&^& streamlit run app.py
echo.
pause
