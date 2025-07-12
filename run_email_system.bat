@echo off
echo Email Segregation System Launcher
echo ===================================
echo.
echo Choose run mode:
echo 1. Continuous Mode (check every minute - recommended)
echo 2. Single Run Mode (run once and exit)
echo 3. Custom interval continuous mode
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting in Continuous Mode (1 minute intervals)...
    python main.py --mode continuous --interval 60
) else if "%choice%"=="2" (
    echo Starting in Single Run Mode...
    python main.py --mode once
) else if "%choice%"=="3" (
    set /p interval="Enter check interval in seconds: "
    echo Starting in Continuous Mode with %interval% second intervals...
    python main.py --mode continuous --interval %interval%
) else (
    echo Invalid choice. Defaulting to Continuous Mode...
    python main.py --mode continuous --interval 60
)

echo.
echo Press any key to exit...
pause >nul
