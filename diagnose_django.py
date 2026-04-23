import os
import sys
import subprocess
import time
import requests

def test_django_setup():
    print("=== Django Diagnostic Test ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError as e:
        print(f"Django import error: {e}")
        return False
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projecthub.settings')
        django.setup()
        print("Django setup successful")
        
        # Test basic Django functionality
        from django.core.management import call_command
        result = call_command('check', verbosity=0)
        print("Django check completed")
        
        return True
    except Exception as e:
        print(f"Django setup error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_startup():
    print("\n=== Testing Server Startup ===")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("Server process started, PID:", process.pid)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is responding
        try:
            response = requests.get('http://127.0.0.1:8000', timeout=5)
            print(f"Server response status: {response.status_code}")
            print("Server is running and responding!")
            
            # Terminate server
            process.terminate()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Server not responding: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"Server startup error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if test_django_setup():
        print("\n=== Starting Server Test ===")
        if test_server_startup():
            print("\n=== SUCCESS: Django server is working ===")
        else:
            print("\n=== FAILED: Django server test failed ===")
    else:
        print("\n=== FAILED: Django setup failed ===")
