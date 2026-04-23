#!/usr/bin/env python
"""
FINAL DJANGO SERVER SOLUTION
This script provides multiple methods to start Django server with comprehensive error handling
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def method_1_direct_command():
    """Method 1: Direct Django management command"""
    print("=== Method 1: Direct Django Command ===")
    try:
        # Change to project directory
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # Set environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projecthub.settings')
        
        # Import and setup Django
        import django
        django.setup()
        
        # Execute runserver command directly
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
        
    except Exception as e:
        print(f"Method 1 failed: {e}")
        return False
    return True

def method_2_subprocess():
    """Method 2: Subprocess with output capture"""
    print("=== Method 2: Subprocess Approach ===")
    try:
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # Start server as subprocess
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print("Server started with PID:", process.pid)
        print("Server should be available at: http://127.0.0.1:8000")
        
        # Try to open browser
        try:
            webbrowser.open('http://127.0.0.1:8000')
            print("Browser opened automatically")
        except:
            print("Could not open browser automatically")
        
        # Monitor output
        try:
            for line in process.stdout:
                print(line.strip())
        except KeyboardInterrupt:
            print("\nStopping server...")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"Method 2 failed: {e}")
        return False
    return True

def method_3_system_command():
    """Method 3: System command approach"""
    print("=== Method 3: System Command ===")
    try:
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # Use os.system to run command
        command = f'"{sys.executable}" manage.py runserver 127.0.0.1:8000'
        print(f"Running: {command}")
        
        result = os.system(command)
        return result == 0
        
    except Exception as e:
        print(f"Method 3 failed: {e}")
        return False

def main():
    print("=== DJANGO SERVER STARTER ===")
    print(f"Python: {sys.executable}")
    print(f"Project: {Path(__file__).parent}")
    print(f"Django: {os.environ.get('DJANGO_SETTINGS_MODULE', 'projecthub.settings')}")
    
    # Test Django import
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError:
        print("ERROR: Django not installed. Run: pip install django")
        return 1
    
    # Try each method
    methods = [
        ("Direct Django Command", method_1_direct_command),
        ("Subprocess Approach", method_2_subprocess),
        ("System Command", method_3_system_command)
    ]
    
    for name, method in methods:
        print(f"\n--- Trying {name} ---")
        try:
            if method():
                print(f"{name} succeeded!")
                return 0
            else:
                print(f"{name} failed")
        except KeyboardInterrupt:
            print("\nServer stopped by user")
            return 0
        except Exception as e:
            print(f"{name} error: {e}")
    
    print("\n=== ALL METHODS FAILED ===")
    print("Please try manual startup:")
    print("1. cd e:\\ProjectHub")
    print("2. python manage.py runserver")
    print("3. Open http://127.0.0.1:8000 in browser")
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
