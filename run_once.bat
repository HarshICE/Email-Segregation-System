@echo off
echo Starting Email Segregation System in SINGLE-RUN MODE
echo Will check for emails once and exit
echo.
python main.py --mode once
echo.
echo Press any key to exit...
pause >nul
