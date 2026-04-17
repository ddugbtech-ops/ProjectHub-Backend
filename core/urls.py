from django.urls import path
from . import views_auth, views_teacher, views_student

urlpatterns = [
    path('', views_auth.home, name='home'),
    path('logout/', views_auth.user_logout, name='logout'),
    
    # Teacher Auth
    path('teacher/register/', views_auth.teacher_register, name='teacher_register'),
    path('teacher/login/', views_auth.teacher_login, name='teacher_login'),
    
    # Student Auth
    path('student/register/', views_auth.student_register, name='student_register'),
    path('student/login/', views_auth.student_login, name='student_login'),
    
    # Teacher Portal
    path('teacher/dashboard/', views_teacher.dashboard, name='teacher_dashboard'),
    path('teacher/project/create/', views_teacher.create_project, name='create_project'),
    path('teacher/project/<int:project_id>/', views_teacher.project_detail, name='project_detail'),
    path('teacher/project/<int:project_id>/edit/', views_teacher.edit_project, name='edit_project'),
    path('teacher/project/<int:project_id>/add-member/', views_teacher.add_member, name='add_member'),
    path('teacher/project/<int:project_id>/group/create/', views_teacher.create_group, name='create_group'),
    path('teacher/project/<int:project_id>/task/create/', views_teacher.create_task, name='create_task'),
    path('teacher/task/<int:task_id>/edit/', views_teacher.edit_task, name='edit_task'),
    path('teacher/submissions/', views_teacher.view_submissions, name='teacher_submissions'),
    
    # Student Portal
    path('student/dashboard/', views_student.dashboard, name='student_dashboard'),
    path('student/join/', views_student.join_project, name='join_project'),
    path('student/project/<int:project_id>/', views_student.project_detail, name='student_project_detail'),
    path('student/task/<int:task_id>/', views_student.task_detail, name='task_detail'),
    path('student/task/<int:task_id>/submit/', views_student.submit_work, name='submit_work'),
    path('student/progress/', views_student.view_progress, name='student_progress'),
]
