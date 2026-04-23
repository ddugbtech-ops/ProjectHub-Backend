@echo off
echo Starting Django Development Server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

cd /d "e:\ProjectHub"
python manage.py runserver 127.0.0.1:8000

pause
