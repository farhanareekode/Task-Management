from django.urls import path
from .views import (
    dashboard,
    users_list,
    user_create,
admin_create,
    user_update,
admin_update,
    user_delete,
admin_delete,
    admins_list,
    assign_user,
    reports_list,
    task_update_status,
    task_delete,
    task_report,
tasks_view,
user_tasks,

admin_tasks,
admin_reports
)
app_name = "admin_panel"

urlpatterns = [
    path("", dashboard, name="dashboard"),

    path("users/", users_list, name="users"),
    path("admins/", admins_list, name="admins"),

    path("assign/", assign_user, name="assign"),
    path("reports/", reports_list, name="reports"),

    path("users/create/", user_create, name="user-create"),
    path("admins/create/", admin_create, name="admin-create"),

    path("users/<int:user_id>/edit/", user_update, name="user-update"),
    path("admins/<int:user_id>/edit/", admin_update, name="admin-update"),

    path("users/<int:user_id>/delete/", user_delete, name="user-delete"),
    path("users/<int:user_id>/delete/", admin_delete, name="admin-delete"),

    path("tasks/<int:task_id>/update/", task_update_status, name="task-update"),
    path("tasks/<int:task_id>/delete/", task_delete, name="task-delete"),
    path("tasks/<int:task_id>/report/", task_report, name="task-report"),
    path("tasks/", tasks_view, name="tasks"),

    path("admin/tasks/", admin_tasks, name="admin-tasks"),
    path("admin/reports/", admin_reports, name="admin-reports"),

    path("my-tasks/", user_tasks, name="user_task"),

]
