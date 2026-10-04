@echo off
title College Placement Prediction System
echo ========================================================
echo   College Placement Prediction - Web Application
echo   BCA Mini Project (Machine Learning)
echo ========================================================
echo.

set "PY_DIRECT=C:\Users\naidu\AppData\Local\Programs\Python\Python311\python.exe"

if exist "%PY_DIRECT%" (
    set "PYTHON_EXE=%PY_DIRECT%"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Using Python from: %PYTHON_EXE%
echo Starting Flask Web Server...
echo Open your browser and visit: http://127.0.0.1:5000
echo Press Ctrl+C in this terminal window to stop the server.
echo.

"%PYTHON_EXE%" app\app.py

pause
