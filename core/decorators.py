from django.shortcuts import redirect
from django.contrib import messages

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('teacher_login')
        if hasattr(request.user, 'profile') and request.user.profile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Teacher account required.")
        return redirect('home')
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('student_login')
        if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access denied. Student account required.")
        return redirect('home')
    return wrapper
