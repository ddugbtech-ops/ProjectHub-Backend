from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

def teacher_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        allowed_domains = ('.com', '.in', '.gov')
        if not email.endswith(allowed_domains):
            messages.error(request, "Only .com, .in, and .gov emails are allowed.")
            return render(request, 'teacher/register.html')
            
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            UserProfile.objects.create(user=user, role='teacher')
            login(request, user)
            return redirect('teacher_dashboard')
            
    return render(request, 'teacher/register.html')

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if hasattr(user, 'profile') and user.profile.role == 'teacher':
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "This account is not a teacher account.")
        else:
            messages.error(request, "Invalid credentials.")
            
    return render(request, 'teacher/login.html')

def student_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        allowed_domains = ('.com', '.in', '.gov')
        if not email.endswith(allowed_domains):
            messages.error(request, "Only .com, .in, and .gov emails are allowed.")
            return render(request, 'student/register.html')
            
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            UserProfile.objects.create(user=user, role='student')
            login(request, user)
            return redirect('student_dashboard')
            
    return render(request, 'student/register.html')

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if hasattr(user, 'profile') and user.profile.role == 'student':
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, "This account is not a student account.")
        else:
            messages.error(request, "Invalid credentials.")
            
    return render(request, 'student/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

from django.core.management import call_command
from django.http import HttpResponse
from django.db import connection
from django.utils.crypto import get_random_string

def run_migrations(request):
    try:
        with connection.cursor() as cursor:
            # Fix core_group
            cursor.execute("SELECT id FROM core_group WHERE join_code IS NULL")
            for row in cursor.fetchall():
                cursor.execute("UPDATE core_group SET join_code = %s WHERE id = %s", [get_random_string(8).upper(), row[0]])
            
            # Fix core_project just in case
            cursor.execute("SELECT id FROM core_project WHERE join_code IS NULL")
            for row in cursor.fetchall():
                cursor.execute("UPDATE core_project SET join_code = %s WHERE id = %s", [get_random_string(8).upper(), row[0]])

        call_command('migrate')
        return HttpResponse("Migrations ran successfully! Your database is now up to date.")
    except Exception as e:
        return HttpResponse(f"Error running migrations: {str(e)}")
