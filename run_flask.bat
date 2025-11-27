@echo off
REM ==== SilverCare Portal Quick Launcher ====

REM 1. Move into your project folder
cd /d "C:\CSCI_275\Project_coding_files\silver-care-initiative"

REM 2. Temporarily allow PowerShell scripts (safe for this session)
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"

REM 3. Activate your virtual environment
call venv\Scripts\activate

REM 4. Run your Flask app
python app.py

REM 5. Keep window open after exit
pause
