from django.urls import path
from .views import (task_list, complete_task,task_report,register_view,login_view)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('user_login/', login_view, name='login'),

    path('task_list/', task_list, name='task-list'),
    path('complete_task/<int:task_id>/', complete_task, name='task-complete'),
    path('task_report/<int:task_id>/report/', task_report, name='task-report'),
]
