@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

:: venv
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)
 call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running the application...
python main.py

:: Deactivate virtual environment
deactivate

echo.
echo Application finished. Press any key to exit.
pause >nul