#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projecthub.settings')
    try:
        django.setup()
        print("Django setup successful")
        print("Django version:", django.get_version())
        
        # Try to run a simple management command
        from django.core.management import call_command
        result = call_command('check', verbosity=0)
        print("Django check completed successfully")
        
        print("Starting Django development server...")
        print("Server should be available at http://127.0.0.1:8000")
        print("Press Ctrl+C to stop the server")
        
        # Run runserver
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
