from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Group, Task, Submission, GroupMember, ProjectMember, ProjectMessage, TeamRating, ProjectSubmission
from .decorators import teacher_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg

@teacher_required
def dashboard(request):
    projects = Project.objects.filter(teacher=request.user)
    return render(request, 'teacher/dashboard.html', {'projects': projects})

@teacher_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        Project.objects.create(name=name, description=description, teacher=request.user, deadline=deadline)
        messages.success(request, "Project created successfully!")
        return redirect('teacher_dashboard')
    return render(request, 'teacher/create_project.html')

@teacher_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    if request.method == 'POST':
        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.deadline = request.POST.get('deadline')
        project.save()
        messages.success(request, "Project updated successfully!")
        return redirect('project_detail', project_id=project.id)
    return render(request, 'teacher/edit_project.html', {'project': project})

@teacher_required
def add_member(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            student = User.objects.get(username=email, profile__role='student')
            ProjectMember.objects.get_or_create(project=project, student=student)
            messages.success(request, f"Added {student.get_full_name()} to the project!")
        except User.DoesNotExist:
            messages.error(request, "Student not found with that email.")
    return redirect('project_detail', project_id=project.id)

@teacher_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    groups = project.groups.all()
    tasks = project.tasks.all().order_by('-deadline')
    
    # Task status counts
    todo_count = tasks.filter(status='pending').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    completed_count = tasks.filter(status='completed').count()
    
    project_members = ProjectMember.objects.filter(project=project).select_related('student')
    
    # Calculate average ratings for each student in this project
    for member in project_members:
        ratings = TeamRating.objects.filter(group__project=project, ratee=member.student)
        if ratings.exists():
            avg_contrib = ratings.aggregate(Avg('contribution'))['contribution__avg']
            avg_comm = ratings.aggregate(Avg('communication'))['communication__avg']
            avg_collab = ratings.aggregate(Avg('collaboration'))['collaboration__avg']
            member.avg_rating = (avg_contrib + avg_comm + avg_collab) / 3
        else:
            member.avg_rating = None

    students_in_groups = GroupMember.objects.filter(group__project=project).values_list('student_id', flat=True)
    unassigned_students = project_members.exclude(student_id__in=students_in_groups)
    messages_list = project.messages.all().order_by('-created_at')
    
    return render(request, 'teacher/project_detail.html', {
        'project': project, 
        'groups': groups, 
        'tasks': tasks,
        'project_members': project_members,
        'unassigned_students': unassigned_students,
        'students_in_groups': students_in_groups,
        'messages': messages_list,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count
    })

@teacher_required
def post_message(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ProjectMessage.objects.create(project=project, user=request.user, content=content)
            messages.success(request, "Message posted to discussion panel.")
    return redirect('project_detail', project_id=project.id)

@teacher_required
def create_group(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    project_members = ProjectMember.objects.filter(project=project)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_students = request.POST.getlist('students')
        leader_id = request.POST.get('leader')
        
        leader = User.objects.get(id=leader_id) if leader_id else None
        group = Group.objects.create(project=project, name=name, leader=leader)
        for student_id in selected_students:
            student = User.objects.get(id=student_id)
            GroupMember.objects.create(group=group, student=student)
            
        messages.success(request, f"Group '{name}' created with {len(selected_students)} members!")
        return redirect('project_detail', project_id=project.id)
        
    already_in_group = set(
        GroupMember.objects.filter(group__project=project).values_list('student_id', flat=True)
    )
    return render(request, 'teacher/create_group.html', {
        'project': project,
        'project_members': project_members,
        'already_in_group': already_in_group,
    })

@teacher_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, teacher=request.user)
    groups = project.groups.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        group_id = request.POST.get('group')
        assigned_to_id = request.POST.get('assigned_to')
        
        group = get_object_or_404(Group, id=group_id) if group_id else None
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        
        Task.objects.create(
            project=project, 
            group=group, 
            assigned_to=assigned_to, 
            name=name, 
            description=description, 
            deadline=deadline
        )
        messages.success(request, f"Task '{name}' assigned to {assigned_to.get_full_name()}!")
        return redirect('project_detail', project_id=project.id)
    
    group_data = []
    for g in groups:
        members = GroupMember.objects.filter(group=g).select_related('student')
        group_data.append({
            'group': g,
            'members': [m.student for m in members]
        })
        
    return render(request, 'teacher/create_task.html', {
        'project': project, 
        'groups': groups,
        'group_data': group_data,
        'project_members': ProjectMember.objects.filter(project=project).select_related('student')
    })

@teacher_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__teacher=request.user)
    if request.method == 'POST':
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.deadline = request.POST.get('deadline')
        task.status = request.POST.get('status')
        task.save()
        messages.success(request, "Task updated successfully!")
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'teacher/edit_task.html', {'task': task})

@teacher_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, project__teacher=request.user)
    members = GroupMember.objects.filter(group=group).select_related('student', 'student__profile')
    tasks = group.tasks.all().order_by('-deadline')
    
    member_data = []
    for member in members:
        ratings = TeamRating.objects.filter(group=group, ratee=member.student)
        if ratings.exists():
            avg_contrib = ratings.aggregate(Avg('contribution'))['contribution__avg']
            avg_comm = ratings.aggregate(Avg('communication'))['communication__avg']
            avg_collab = ratings.aggregate(Avg('collaboration'))['collaboration__avg']
            avg_rating = (avg_contrib + avg_comm + avg_collab) / 3
        else:
            avg_rating = None
            
        member_data.append({
            'student': member.student,
            'profile': member.student.profile if hasattr(member.student, 'profile') else None,
            'is_leader': group.leader == member.student,
            'avg_rating': avg_rating,
        })
        
    return render(request, 'teacher/group_detail.html', {
        'group': group,
        'member_data': member_data,
        'tasks': tasks,
    })

@teacher_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, project__teacher=request.user)
    project_members = ProjectMember.objects.filter(project=group.project)
    current_members = group.members.values_list('student_id', flat=True)
    
    if request.method == 'POST':
        group.name = request.POST.get('name')
        leader_id = request.POST.get('leader')
        selected_students = request.POST.getlist('students')
        
        if leader_id:
            group.leader = User.objects.get(id=leader_id)
        group.save()
        
        # Update members
        group.members.all().delete()
        for student_id in selected_students:
            student = User.objects.get(id=student_id)
            GroupMember.objects.create(group=group, student=student)
            
        messages.success(request, f"Group '{group.name}' updated successfully!")
        return redirect('project_detail', project_id=group.project.id)
        
    return render(request, 'teacher/edit_group.html', {
        'group': group,
        'project_members': project_members,
        'current_members': current_members
    })

@teacher_required
def view_submissions(request):
    submissions = Submission.objects.filter(task__project__teacher=request.user).order_by('-submitted_at')
    final_submissions = ProjectSubmission.objects.filter(project__teacher=request.user).order_by('-submitted_at')
    return render(request, 'teacher/submissions.html', {
        'submissions': submissions,
        'final_submissions': final_submissions
    })
