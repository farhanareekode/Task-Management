from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserAdminMap
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseForbidden
# Create your views here.


@login_required
def dashboard(request):
    user = request.user

    user = request.user

    # ================= SUPER ADMIN =================
    if user.is_superuser:
        users_count = User.objects.filter(is_superuser=False).count()

        admins_count = User.objects.filter(
            is_staff=True,
            is_superuser=False
        ).count()

        tasks_count = Task.objects.count()

        completed_tasks = Task.objects.filter(
            status="Completed"
        ).count()

        return render(
            request,
            "admin_panel/superadmin_dashboard.html",
            {
                "users_count": users_count,
                "admins_count": admins_count,
                "tasks_count": tasks_count,
                "completed_tasks": completed_tasks,
            }
        )

    # ================= ADMIN =================
    if user.is_staff and not user.is_superuser:
        users_count = User.objects.filter(
            admin_mapping__admin=user
        ).count()

        tasks_qs = Task.objects.filter(
            assigned_to__admin_mapping__admin=user
        )

        tasks_count = tasks_qs.count()

        completed_tasks = tasks_qs.filter(
            status="Completed"
        ).count()

        pending_tasks = tasks_qs.exclude(
            status="Completed"
        ).count()

        return render(
            request,
            "admin_panel/admin_dashboard.html",
            {
                "users_count": users_count,
                "tasks_count": tasks_count,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
            }
        )
    tasks = Task.objects.filter(assigned_to=user)

    completed_tasks = tasks.filter(status="completed")
    pending_tasks = tasks.exclude(status="completed")  # safer than "pending"

    return render(
        request,
        "admin_panel/user_dashboard.html",
        {
            # LISTS (for looping)
            "tasks": tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,

            # COUNTS (for cards)
            "total_count": tasks.count(),
            "completed_count": completed_tasks.count(),
            "pending_count": pending_tasks.count(),
        }
    )


@login_required
def users_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = User.objects.filter(
        is_staff=False,
        is_superuser=False
    )

    return render(
        request,
        "admin_panel/users.html",
        {"users": users}
    )

@login_required
def admins_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    admins = User.objects.filter(
        is_staff=True,
        is_superuser=False
    )

    return render(
        request,
        "admin_panel/admins.html",
        {"admins": admins}
    )





@login_required
def user_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    admins = User.objects.filter(is_staff=True, is_superuser=False)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role")
        admin_id = request.POST.get("admin")

        errors = []

        # ===== USERNAME VALIDATION =====
        if not username:
            errors.append("Username is required.")
        elif len(username) < 4:
            errors.append("Username must be at least 4 characters.")
        elif User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        # ===== EMAIL VALIDATION =====
        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Invalid email format.")

            if User.objects.filter(email=email).exists():
                errors.append("Email already exists.")

        # ===== PASSWORD VALIDATION =====
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        # ===== ROLE VALIDATION =====
        if role not in ("user", "admin"):
            errors.append("Invalid role selection.")

        # ===== ADMIN ASSIGNMENT VALIDATION =====
        if role == "user":
            if not admin_id:
                errors.append("Admin assignment is required for users.")
            elif not admins.filter(id=admin_id).exists():
                errors.append("Selected admin is invalid.")

        if errors:
            return render(
                request,
                "admin_panel/user_form.html",
                {
                    "errors": errors,
                    "admins": admins,
                    "role": "user",
                }
            )

        # ===== ATOMIC CREATION =====
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            if role == "admin":
                user.is_staff = True
                user.save()
            else:
                UserAdminMap.objects.create(
                    user=user,
                    admin_id=int(admin_id)
                )

        return redirect("admin_panel:users")

    return render(
        request,
        "admin_panel/user_form.html",
        {
            "admins": admins,
            "role": "user",
        }
    )

@login_required
def admin_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "admin_panel/user_form.html",
                {
                    "error": "Username already exists",
                    "role": "admin",
                }
            )

        admin = User.objects.create_user(
            username=username,
            password=password,
            is_staff=True,
        )

        return redirect("admin_panel:admins")

    return render(
        request,
        "admin_panel/user_form.html",
        {"role": "admin"}
    )


@login_required
def user_update(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(
        User,
        id=user_id,
        is_staff=False,
        is_superuser=False
    )

    admins = User.objects.filter(is_staff=True, is_superuser=False)
    mapping = UserAdminMap.objects.filter(user=user).first()

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email", "")
        admin_id = request.POST.get("admin")

        if User.objects.exclude(id=user.id).filter(username=username).exists():
            return render(
                request,
                "admin_panel/user_update.html",
                {
                    "error": "Username already exists",
                    "user_obj": user,
                    "admins": admins,
                    "assigned_admin": mapping.admin.id if mapping else None,
                    "role": "user",
                }
            )

        user.username = username
        user.email = email
        user.save()

        if admin_id:
            UserAdminMap.objects.update_or_create(
                user=user,
                defaults={"admin_id": int(admin_id)}
            )

        return redirect("admin_panel:users")

    return render(
        request,
        "admin_panel/user_update.html",
        {
            "user_obj": user,
            "admins": admins,
            "assigned_admin": mapping.admin.id if mapping else None,
            "role": "user",
        }
    )


@login_required
def admin_update(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    admin = get_object_or_404(
        User,
        id=user_id,
        is_staff=True,
        is_superuser=False
    )

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email", "")

        if User.objects.exclude(id=admin.id).filter(username=username).exists():
            return render(
                request,
                "admin_panel/user_update.html",
                {
                    "error": "Username already exists",
                    "user_obj": admin,
                    "role": "admin",
                }
            )

        admin.username = username
        admin.email = email
        admin.save()

        return redirect("admin_panel:admins")

    return render(
        request,
        "admin_panel/user_update.html",
        {
            "user_obj": admin,
            "role": "admin",
        }
    )


@login_required
def user_delete(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    User.objects.filter(
        id=user_id,
        is_staff=False,
        is_superuser=False
    ).delete()

    return redirect("admin_panel:users")

@login_required
def admin_delete(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    User.objects.filter(
        id=user_id,
        is_staff=True,
        is_superuser=False
    ).delete()

    return redirect("admin_panel:admins")


@login_required
def admins_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(
        request,
        "admin_panel/admins.html",
        {"admins": admins}
    )


@login_required
def assign_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    return render(request, "admin_panel/assign_user.html")



@login_required
def reports_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    tasks = Task.objects.filter(status="Completed").select_related("assigned_to")

    return render(
        request,
        "admin_panel/task_reports.html",
        {"tasks": tasks}
    )


@login_required
def tasks_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    tasks = Task.objects.select_related("assigned_to").all()

    if request.method == "POST":
        action = request.POST.get("action")

        # ===== CREATE =====
        if action == "create_task":
            Task.objects.create(
                title=request.POST["title"],
                description=request.POST["description"],
                assigned_to_id=int(request.POST["assigned_to"]),
                status=request.POST["status"],
            )
            return redirect("admin_panel:tasks")

        # ===== FULL UPDATE =====
        if action == "update_task":
            task = get_object_or_404(Task, id=request.POST.get("task_id"))

            task.title = request.POST["title"]
            task.description = request.POST["description"]
            task.assigned_to_id = int(request.POST["assigned_to"])
            task.status = request.POST["status"]

            task.save()
            return redirect("admin_panel:tasks")

    return render(
        request,
        "admin_panel/tasks.html",
        {
            "users": users,
            "tasks": tasks,
        }
    )



@login_required
def tasks_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    tasks = Task.objects.select_related("assigned_to").all()

    return render(
        request,
        "admin_panel/tasks.html",
        {"tasks": tasks}
    )

@login_required
def task_update_status(request, task_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.status = request.POST["status"]
        task.save()

    return redirect("admin_panel:tasks")

@login_required
def task_delete(request, task_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    Task.objects.filter(id=task_id).delete()
    return redirect("admin_panel:tasks")

@login_required
def task_report(request, task_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    task = get_object_or_404(Task, id=task_id, status="Completed")

    return render(
        request,
        "admin_panel/task_report.html",
        {"task": task}
    )

@login_required
def task_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = User.objects.filter(is_superuser=False)

    if request.method == "POST":
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            assigned_to_id=request.POST["assigned_to"],
            status=request.POST["status"],
        )
        return redirect("admin_panel:tasks")

    return render(
        request,
        "admin_panel/task_form.html",
        {"users": users}
    )


####### ADMIN ########




@login_required
def admin_tasks(request):
    if not request.user.is_staff or request.user.is_superuser:
        return HttpResponseForbidden("Admins only")

    users = User.objects.filter(
        admin_mapping__admin=request.user
    ).prefetch_related("tasks")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_status":
            task = get_object_or_404(
                Task,
                id=request.POST.get("task_id"),
                assigned_to__admin_mapping__admin=request.user
            )

            new_status = request.POST.get("status")
            if new_status not in dict(Task.STATUS_CHOICES):
                return HttpResponseForbidden("Invalid status")

            task.status = new_status
            task.save()

            return redirect("admin_panel:admin-tasks")

    return render(
        request,
        "admin_panel/admin_tasks.html",
        {"users": users}
    )


@login_required
def admin_reports(request):
    if not request.user.is_staff or request.user.is_superuser:
        return HttpResponseForbidden()

    tasks = Task.objects.filter(
        status="Completed"
    ).select_related("assigned_to")

    return render(
        request,
        "admin_panel/admin_reports.html",
        {"tasks": tasks}
    )

#### user#####






@login_required
def user_tasks(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)

    if request.method == "POST":
        task = get_object_or_404(
            Task,
            id=request.POST.get("task_id"),
            assigned_to=user,
        )

        new_status = request.POST.get("status")

        if new_status == "Completed":
            report = request.POST.get("completion_report", "").strip()
            hours = request.POST.get("worked_hours")

            if not report or not hours:
                return render(
                    request,
                    "admin_panel/user_tasks.html",
                    {
                        "tasks": tasks,
                        "error": "Report and worked hours are required to complete a task.",
                    }
                )

            task.completion_report = report
            task.worked_hours = hours

        task.status = new_status
        task.save()

        return redirect("admin_panel:user_task")

    return render(
        request,
        "admin_panel/user_task.html",
        {"tasks": tasks}
    )
