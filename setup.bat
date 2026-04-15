@echo off
REM Pitch Visualizer - Setup Script for Windows

echo.
echo ╔═══════════════════════════════════════╗
echo ║   Pitch Visualizer - Setup Script     ║
echo ╚═══════════════════════════════════════╝
echo.

REM Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found

REM Create virtual environment
echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo ✓ Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Install requirements
echo.
echo [4/4] Installing dependencies (this may take 5-10 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo ═══════════════════════════════════════
echo ✨ Setup complete!
echo ═══════════════════════════════════════
echo.
echo To start the app, run:
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo.
pause
