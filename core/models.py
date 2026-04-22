from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    join_code = models.CharField(max_length=8, unique=True, blank=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.join_code:
            self.join_code = get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Group(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='led_groups', null=True, blank=True)
    join_code = models.CharField(max_length=8, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.join_code:
            self.join_code = get_random_string(8).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')

    class Meta:
        unique_together = ('project', 'student')

    def __str__(self):
        return f"{self.student.username} in {self.project.name}"

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')

    class Meta:
        unique_together = ('group', 'student')

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateField()

    def __str__(self):
        return self.name

class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.task.name} by {self.student.username}"

class ProjectMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in {self.project.name}"

class TeamRating(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    
    # Detailed Criteria
    contribution = models.IntegerField(default=5)
    communication = models.IntegerField(default=5)
    collaboration = models.IntegerField(default=5)
    
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'rater', 'ratee')

    @property
    def average_score(self):
        return (self.contribution + self.communication + self.collaboration) / 3

    def __str__(self):
        return f"{self.rater.username} rated {self.ratee.username}"

class ProjectSubmission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='final_submissions')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='final_submissions', null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_project_submissions')
    file = models.FileField(upload_to='project_submissions/', null=True, blank=True)
    github_link = models.URLField(blank=True, null=True)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Final Submission for {self.project.name} by {self.student.username}"
