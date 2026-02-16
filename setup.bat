@echo off
REM Setup script for Building Energy Data API on Windows
REM Usage: setup.bat

echo.
echo 🚀 Setting up Building Energy Data API...
echo.

REM Check Python version
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)

echo.
echo 📦 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    exit /b 1
)
echo ✅ Virtual environment created

echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✅ Dependencies installed

echo.
echo ✨ Setup complete!
echo.
echo To run the API:
echo   python main.py
echo.
echo To run tests:
echo   pytest test_main.py -v
echo.
echo To run example usage:
echo   python example_usage.py
echo.
echo View API docs at:
echo   http://localhost:8000/docs
echo.
pause
