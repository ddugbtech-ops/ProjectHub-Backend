from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_auth, views_teacher, views_student, views_profile

urlpatterns = [
    path('migrate-db-run/', views_auth.run_migrations, name='run_migrations'),
    path('', views_auth.home, name='home'),
    path('logout/', views_auth.user_logout, name='logout'),
    
    # Profile
    path('profile/', views_profile.view_profile, name='view_profile'),
    path('profile/edit/', views_profile.edit_profile, name='edit_profile'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
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
    path('teacher/project/<int:project_id>/group/create/', views_teacher.create_group, name='teacher_create_group'),
    path('teacher/project/<int:project_id>/task/create/', views_teacher.create_task, name='create_task'),
    path('teacher/task/<int:task_id>/edit/', views_teacher.edit_task, name='edit_task'),
    path('teacher/group/<int:group_id>/', views_teacher.group_detail, name='teacher_group_detail'),
    path('teacher/group/<int:group_id>/edit/', views_teacher.edit_group, name='edit_group'),
    path('teacher/project/<int:project_id>/message/', views_teacher.post_message, name='teacher_post_message'),
    path('teacher/submissions/', views_teacher.view_submissions, name='teacher_submissions'),
    
    # Student Portal
    path('student/dashboard/', views_student.dashboard, name='student_dashboard'),
    path('student/join/', views_student.join_project, name='join_project'),
    path('student/project/<int:project_id>/', views_student.project_detail, name='student_project_detail'),
    path('student/project/<int:project_id>/submit/', views_student.submit_project, name='submit_project_final'),
    path('student/project/<int:project_id>/message/', views_student.post_message, name='student_post_message'),
    path('student/project/<int:project_id>/group/create/', views_student.create_group, name='create_group'),
    path('student/group/join/', views_student.join_group, name='join_group'),
    path('student/group/<int:group_id>/', views_student.group_detail, name='student_group_detail'),
    path('student/group/<int:group_id>/edit/', views_student.edit_group, name='student_edit_group'),
    path('student/group/<int:group_id>/rate/<int:user_id>/', views_student.rate_member, name='rate_member'),
    path('student/group/<int:group_id>/task/create/', views_student.create_group_task, name='create_group_task'),
    path('student/task/<int:task_id>/', views_student.task_detail, name='task_detail'),
    path('student/task/<int:task_id>/submit/', views_student.submit_work, name='submit_work'),
    path('student/progress/', views_student.view_progress, name='student_progress'),
]
