@echo off
REM Git setup and push script for Building Energy Data API
REM This script will configure git and push to a repository

cd /d e:\building-energy-api

echo.
echo ====================================
echo Building Energy Data API - Git Setup
echo ====================================
echo.

REM Configure git (if first time)
echo Configuring Git...
git config --global user.name "Your Name" 2>nul || (
    echo Please configure git first:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "your@email.com"
)

REM Initialize repository
echo.
echo Initializing git repository...
git init

REM Add all files
echo.
echo Adding files to git...
git add .

REM Create initial commit
echo.
echo Creating commit...
git commit -m "Initial commit: Building Energy Data API with FastAPI"

REM Show status
echo.
echo ====================================
echo Git Status:
echo ====================================
git status

echo.
echo.
echo ====================================
echo NEXT STEPS:
echo ====================================
echo.
echo 1. Create a repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name: building-energy-api
echo    - Click "Create repository"
echo.
echo 2. Copy the repository URL (https://github.com/YOUR_USERNAME/building-energy-api.git)
echo.
echo 3. Run these commands:
echo    cd e:\building-energy-api
echo    git remote add origin https://github.com/YOUR_USERNAME/building-energy-api.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo.
pause
