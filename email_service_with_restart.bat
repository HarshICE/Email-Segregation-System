@echo off
title Email Segregation System - Auto Restart
echo ====================================================
echo Email Segregation System with Auto-Restart
echo ====================================================
echo This will run the email system continuously and
echo automatically restart it if it stops for any reason.
echo.
echo Press Ctrl+C to stop completely
echo ====================================================
echo.

:loop
echo [%date% %time%] Starting Email Segregation System...
python main.py --mode continuous --interval 30

echo.
echo [%date% %time%] System stopped. Restarting in 10 seconds...
echo Press Ctrl+C to abort restart...
timeout /t 10
echo.
goto loop
