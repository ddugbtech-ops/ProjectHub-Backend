from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Group, Task, Submission, GroupMember, ProjectMember
from .decorators import student_required
from django.contrib import messages

@student_required
def dashboard(request):
    joined_projects = Project.objects.filter(members__student=request.user).distinct()
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-deadline')
    return render(request, 'student/dashboard.html', {'projects': joined_projects, 'tasks': tasks})

@student_required
def join_project(request):
    if request.method == 'POST':
        join_code = request.POST.get('join_code')
        try:
            project = Project.objects.get(join_code=join_code)
            ProjectMember.objects.get_or_create(project=project, student=request.user)
            messages.success(request, f"Successfully joined {project.name}!")
            return redirect('student_dashboard')
        except Project.DoesNotExist:
            messages.error(request, "Invalid join code.")
    return render(request, 'student/join_project.html')

@student_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, members__student=request.user)
    groups = project.groups.all()
    tasks = project.tasks.all().order_by('-deadline')
    project_members = ProjectMember.objects.filter(project=project).select_related('student')
    
    # Calculate progress for this student in this project
    student_tasks = tasks.filter(assigned_to=request.user)
    completed_count = student_tasks.filter(status='completed').count()
    total_count = student_tasks.count()
    progress = (completed_count / total_count * 100) if total_count > 0 else 0
    
    return render(request, 'student/project_detail.html', {
        'project': project,
        'groups': groups,
        'tasks': tasks,
        'project_members': project_members,
        'progress': progress,
        'student_tasks': student_tasks
    })

@student_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__members__student=request.user)
    return render(request, 'student/task_detail.html', {'task': task})

@student_required
def submit_work(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        description = request.POST.get('description')
        Submission.objects.create(task=task, student=request.user, description=description)
        task.status = 'completed'
        task.save()
        messages.success(request, f"Task '{task.name}' committed successfully!")
        return redirect('student_dashboard')
    return render(request, 'student/submit_work.html', {'task': task})

@student_required
def view_progress(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    completed_tasks = tasks.filter(status='completed').count()
    total_tasks = tasks.count()
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return render(request, 'student/progress.html', {'tasks': tasks, 'progress': progress})
