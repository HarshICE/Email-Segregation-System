@echo off
echo Starting Email Segregation System in CONTINUOUS MODE
echo Will check for new emails every 60 seconds (1 minute)
echo Press Ctrl+C to stop the system gracefully
echo.
python main.py --mode continuous --interval 60
