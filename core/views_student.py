from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Group, Task, Submission, GroupMember, ProjectMember, ProjectMessage, TeamRating, ProjectSubmission
from .decorators import student_required
from django.contrib import messages
from django.contrib.auth.models import User

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
    
    # Check if user is in a group for this project
    user_group_member = GroupMember.objects.filter(group__project=project, student=request.user).first()
    user_group = user_group_member.group if user_group_member else None
    
    groups = project.groups.all()
    tasks = project.tasks.all().order_by('-deadline')
    project_members = ProjectMember.objects.filter(project=project).select_related('student')
    
    # Calculate progress for this student in this project
    student_tasks = tasks.filter(assigned_to=request.user)
    completed_count = student_tasks.filter(status='completed').count()
    total_count = student_tasks.count()
    progress = (completed_count / total_count * 100) if total_count > 0 else 0
    
    messages_list = project.messages.all().order_by('-created_at')
    
    # Check for final project submission
    final_submission = ProjectSubmission.objects.filter(project=project, student=request.user).first()
    if not final_submission and user_group:
        final_submission = ProjectSubmission.objects.filter(project=project, group=user_group).first()

    return render(request, 'student/project_detail.html', {
        'project': project,
        'groups': groups,
        'tasks': tasks,
        'project_members': project_members,
        'progress': progress,
        'student_tasks': student_tasks,
        'user_group': user_group,
        'messages': messages_list,
        'final_submission': final_submission
    })

@student_required
def submit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, members__student=request.user)
    user_group = Group.objects.filter(project=project, members__student=request.user).first()
    
    if request.method == 'POST':
        description = request.POST.get('description')
        github_link = request.POST.get('github_link')
        file = request.FILES.get('file')
        
        ProjectSubmission.objects.create(
            project=project,
            group=user_group,
            student=request.user,
            description=description,
            github_link=github_link,
            file=file
        )
        messages.success(request, f"Final project submission for '{project.name}' successful!")
        return redirect('student_project_detail', project_id=project.id)
        
    return render(request, 'student/submit_project.html', {'project': project})

@student_required
def post_message(request, project_id):
    project = get_object_or_404(Project, id=project_id, members__student=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ProjectMessage.objects.create(project=project, user=request.user, content=content)
            messages.success(request, "Query/Message posted successfully.")
    return redirect('student_project_detail', project_id=project.id)

@student_required
def create_group(request, project_id):
    project = get_object_or_404(Project, id=project_id, members__student=request.user)
    # Check if student is already in a group for this project
    if GroupMember.objects.filter(group__project=project, student=request.user).exists():
        messages.error(request, "You are already in a group for this project.")
        return redirect('student_project_detail', project_id=project.id)
        
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = Group.objects.create(project=project, name=name, leader=request.user)
            GroupMember.objects.create(group=group, student=request.user)
            messages.success(request, f"Group '{name}' created! Share the join code: {group.join_code}")
            return redirect('student_group_detail', group_id=group.id)
            
    return render(request, 'student/create_group.html', {'project': project})

@student_required
def join_group(request):
    if request.method == 'POST':
        join_code = request.POST.get('join_code')
        try:
            group = Group.objects.get(join_code=join_code)
            # Check if student is in the project
            if not ProjectMember.objects.filter(project=group.project, student=request.user).exists():
                messages.error(request, "You must be a member of the project to join this group.")
                return redirect('student_dashboard')
                
            # Check if student is already in a group for this project
            if GroupMember.objects.filter(group__project=group.project, student=request.user).exists():
                messages.error(request, "You are already in a group for this project.")
                return redirect('student_project_detail', project_id=group.project.id)
                
            GroupMember.objects.create(group=group, student=request.user)
            messages.success(request, f"Successfully joined group '{group.name}'!")
            return redirect('student_group_detail', group_id=group.id)
        except Group.DoesNotExist:
            messages.error(request, "Invalid group join code.")
            
    return render(request, 'student/join_group.html')

@student_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, members__student=request.user)
    members = group.members.all().select_related('student')
    tasks = group.tasks.all().order_by('-deadline')
    is_leader = (group.leader == request.user)
    
    # Get existing ratings given by this user in this group
    given_ratings = TeamRating.objects.filter(group=group, rater=request.user).values_list('ratee_id', flat=True)
    
    # Get average ratings for all members in this group
    from django.db.models import Avg
    member_data = []
    for m in members:
        ratings = TeamRating.objects.filter(group=group, ratee=m.student)
        if ratings.exists():
            avg_contrib = ratings.aggregate(Avg('contribution'))['contribution__avg']
            avg_comm = ratings.aggregate(Avg('communication'))['communication__avg']
            avg_collab = ratings.aggregate(Avg('collaboration'))['collaboration__avg']
            avg_rating = (avg_contrib + avg_comm + avg_collab) / 3
        else:
            avg_rating = None
            
        member_data.append({
            'member': m,
            'avg_rating': avg_rating,
            'has_been_rated': m.student.id in given_ratings
        })
        
    return render(request, 'student/group_detail.html', {
        'group': group,
        'members': members,
        'tasks': tasks,
        'is_leader': is_leader,
        'member_data': member_data
    })

@student_required
def rate_member(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id, members__student=request.user)
    ratee = get_object_or_404(User, id=user_id)
    
    if not GroupMember.objects.filter(group=group, student=ratee).exists():
        messages.error(request, "User is not in your group.")
        return redirect('student_group_detail', group_id=group.id)
        
    if request.user == ratee:
        messages.error(request, "You cannot rate yourself.")
        return redirect('student_group_detail', group_id=group.id)
        
    if request.method == 'POST':
        contribution = request.POST.get('contribution')
        communication = request.POST.get('communication')
        collaboration = request.POST.get('collaboration')
        comment = request.POST.get('comment')
        
        TeamRating.objects.update_or_create(
            group=group, rater=request.user, ratee=ratee,
            defaults={
                'contribution': contribution,
                'communication': communication,
                'collaboration': collaboration,
                'comment': comment
            }
        )
        
        messages.success(request, f"Evaluation for {ratee.get_full_name()} submitted!")
        return redirect('student_group_detail', group_id=group.id)
        
    return render(request, 'student/rate_member.html', {
        'group': group,
        'ratee': ratee
    })

@student_required
def create_group_task(request, group_id):
    group = get_object_or_404(Group, id=group_id, leader=request.user)
    members = group.members.all().select_related('student')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        assigned_to_id = request.POST.get('assigned_to')
        
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        # Verify assigned student is in the group
        if not GroupMember.objects.filter(group=group, student=assigned_to).exists():
            messages.error(request, "Assigned student must be a member of your group.")
        else:
            Task.objects.create(
                project=group.project,
                group=group,
                assigned_to=assigned_to,
                name=name,
                description=description,
                deadline=deadline
            )
            messages.success(request, f"Task '{name}' assigned to {assigned_to.get_full_name()}!")
            return redirect('student_group_detail', group_id=group.id)
            
    return render(request, 'student/create_task.html', {
        'group': group,
        'members': [m.student for m in members]
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
        file = request.FILES.get('file')
        Submission.objects.create(task=task, student=request.user, description=description, file=file)
        task.status = 'completed'
        task.save()
        messages.success(request, f"Task '{task.name}' committed successfully!")
        return redirect('student_dashboard')
    return render(request, 'student/submit_work.html', {'task': task})

@student_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, leader=request.user)
    
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.save()
        messages.success(request, "Group name updated!")
        return redirect('student_group_detail', group_id=group.id)
        
    return render(request, 'student/edit_group.html', {'group': group})

@student_required
def view_progress(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    completed_tasks = tasks.filter(status='completed').count()
    todo_count = tasks.filter(status='todo').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    total_tasks = tasks.count()
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return render(request, 'student/progress.html', {
        'tasks': tasks, 
        'progress': progress,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_tasks
    })
