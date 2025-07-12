@echo off
echo Setting up Email Segregation System for reliable operation
echo.

echo Option 1: Run as Windows Scheduled Task (Restart every hour)
echo This will restart the system every hour to ensure reliability
echo.
echo To set up:
echo 1. Open Task Scheduler
echo 2. Create Basic Task
echo 3. Name: "Email Segregation System"
echo 4. Trigger: Daily, repeat every 1 hour
echo 5. Action: Start a program
echo 6. Program: python
echo 7. Arguments: main.py --mode continuous --interval 60
echo 8. Start in: %cd%

echo.
echo Option 2: Use NSSM (Non-Sucking Service Manager) to run as Windows Service
echo Download NSSM from: https://nssm.cc/download
echo Then run: nssm install EmailSegregationSystem
echo.

echo Option 3: Use a batch file with auto-restart
echo This batch file will automatically restart the system if it stops:

echo.
echo @echo off > email_service_with_restart.bat
echo :loop >> email_service_with_restart.bat
echo echo Starting Email Segregation System... >> email_service_with_restart.bat
echo python main.py --mode continuous --interval 60 >> email_service_with_restart.bat
echo echo System stopped. Restarting in 10 seconds... >> email_service_with_restart.bat
echo timeout /t 10 >> email_service_with_restart.bat
echo goto loop >> email_service_with_restart.bat

echo.
echo Auto-restart batch file created: email_service_with_restart.bat
echo Run this file to start the system with automatic restart on failure.

pause
