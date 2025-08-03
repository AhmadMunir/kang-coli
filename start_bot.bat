@echo off
echo Starting PMO Recovery Bot...
echo.

cd /d "d:\github.com\kang-coli"

echo Testing Python environment...
python --version
echo.

echo Testing imports...
python quick_check.py
echo.

echo Starting bot...
python run_bot.py

pause
