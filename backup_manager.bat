@echo off
REM PMO Recovery Bot - Backup Management Script for Windows
REM This script provides easy backup management functionality

:MAIN_MENU
cls
echo.
echo ===============================================
echo    PMO Recovery Bot - Backup Management
echo ===============================================
echo.
echo Choose an option:
echo.
echo 1. Create Manual Backup
echo 2. Create Emergency Backup  
echo 3. List All Backups
echo 4. Show Backup Status
echo 5. Database Diagnosis
echo 6. Start Backup Scheduler
echo 7. Restore from Backup
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto CREATE_MANUAL
if "%choice%"=="2" goto CREATE_EMERGENCY
if "%choice%"=="3" goto LIST_BACKUPS
if "%choice%"=="4" goto SHOW_STATUS
if "%choice%"=="5" goto DIAGNOSE
if "%choice%"=="6" goto START_SCHEDULER
if "%choice%"=="7" goto RESTORE_MENU
if "%choice%"=="8" goto EXIT
goto INVALID_CHOICE

:CREATE_MANUAL
cls
echo Creating manual backup...
python backup_manager.py backup --type manual
pause
goto MAIN_MENU

:CREATE_EMERGENCY
cls
echo Creating emergency backup...
python backup_manager.py backup --type emergency
pause
goto MAIN_MENU

:LIST_BACKUPS
cls
echo Listing all available backups...
python backup_manager.py list
pause
goto MAIN_MENU

:SHOW_STATUS
cls
echo Showing backup system status...
python backup_manager.py status
pause
goto MAIN_MENU

:DIAGNOSE
cls
echo Running database diagnosis...
python backup_manager.py diagnose
pause
goto MAIN_MENU

:START_SCHEDULER
cls
echo Starting backup scheduler...
echo WARNING: This will run continuously. Press Ctrl+C to stop.
pause
python backup_manager.py scheduler
pause
goto MAIN_MENU

:RESTORE_MENU
cls
echo.
echo ===============================================
echo             Restore from Backup
echo ===============================================
echo.
echo WARNING: This will replace all current data!
echo Make sure you have the correct backup file path.
echo.
set /p backup_path="Enter backup file path (or 'back' to return): "

if /i "%backup_path%"=="back" goto MAIN_MENU

echo.
echo You are about to restore from:
echo %backup_path%
echo.
echo This will REPLACE ALL CURRENT DATA!
set /p confirm="Are you sure? Type 'YES' to confirm: "

if /i "%confirm%"=="YES" (
    echo Restoring from backup...
    python backup_manager.py restore "%backup_path%" --confirm
) else (
    echo Restore cancelled.
)
pause
goto MAIN_MENU

:INVALID_CHOICE
cls
echo Invalid choice. Please try again.
pause
goto MAIN_MENU

:EXIT
echo.
echo Thank you for using PMO Recovery Bot Backup Management!
echo.
pause
exit

REM Additional utility functions

:CHECK_PYTHON
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)
exit /b 0

:CHECK_BACKUP_MANAGER
if not exist "backup_manager.py" (
    echo ERROR: backup_manager.py not found
    echo Please run this script from the PMO Recovery Bot directory
    pause
    exit /b 1
)
exit /b 0
