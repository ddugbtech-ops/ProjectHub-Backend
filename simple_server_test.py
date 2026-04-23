#!/usr/bin/env python
import os
import sys

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projecthub.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Starting Django server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
