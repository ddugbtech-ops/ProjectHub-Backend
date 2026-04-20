from django.contrib import admin
from .models import UserProfile, Project, Group, ProjectMember, GroupMember, Task, Submission, ProjectMessage, TeamRating, ProjectSubmission

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'join_code', 'deadline')
    search_fields = ('name', 'join_code')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'leader', 'join_code')
    list_filter = ('project',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'group', 'assigned_to', 'status', 'deadline')
    list_filter = ('status', 'project')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'submitted_at')

@admin.register(ProjectMessage)
class ProjectMessageAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
    list_filter = ('project',)

@admin.register(TeamRating)
class TeamRatingAdmin(admin.ModelAdmin):
    list_display = ('group', 'rater', 'ratee', 'average_score', 'created_at')
    list_filter = ('group',)

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'group', 'student', 'submitted_at')
    list_filter = ('project',)

admin.site.register(ProjectMember)
admin.site.register(GroupMember)
