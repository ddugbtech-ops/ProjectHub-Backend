#!/usr/bin/env python
"""
Django Server Starter Script
This script attempts to start the Django development server with proper error handling and output
"""

import os
import sys
import subprocess
import time
import signal
import webbrowser

def main():
    print("=== Django Development Server Starter ===")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        # Change to project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        print(f"Changed to project directory: {project_dir}")
        
        # Check if Django is installed
        import django
        print(f"Django version: {django.get_version()}")
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projecthub.settings')
        
        # Test Django setup
        django.setup()
        print("Django setup completed successfully")
        
        # Check if migrations are up to date
        from django.core.management import call_command
        print("Running Django check...")
        call_command('check', verbosity=1)
        
        print("\n=== Starting Django Development Server ===")
        print("Server will start at: http://127.0.0.1:8000")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        server_process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)
        
        print("Django server process started with PID:", server_process.pid)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Try to open browser
        try:
            webbrowser.open('http://127.0.0.1:8000')
            print("Browser opened to http://127.0.0.1:8000")
        except:
            print("Could not open browser automatically")
        
        # Monitor server output
        try:
            while True:
                output = server_process.stdout.readline()
                if output == '' and server_process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        except KeyboardInterrupt:
            print("\nStopping Django server...")
            server_process.terminate()
            server_process.wait()
            print("Django server stopped")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
