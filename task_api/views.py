from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from admin_panel.models import Task
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user
    """
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    email = request.data.get('email', '').strip()

    if not username or not password:
        return Response(
            {
                "status": False,
                "message": "Username and password are required.",
                "data": None
            },status=status.HTTP_400_BAD_REQUEST )

    if User.objects.filter(username=username).exists():
        return Response(
            {
                "status": False,
                "message": "Username already exists.",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return Response(
        {
            "status": True,
            "message": "User registered successfully.",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user using username and password
    and return JWT access and refresh tokens.
    """
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    # 1. Validate input
    if not username or not password:
        return Response(
            {
                "status": False,
                "message": "Username and password are required.",
                "data": None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {
                "status": False,
                "message": "Invalid username or password.",
                "data": None
            }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response(
            {
                "status": False,
                "message": "User account is disabled.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

    # 3. Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "status": True,
            "message": "Login successful.",
            "data": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        }, status=status.HTTP_200_OK )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    data = [{"id": task.id,"title": task.title,"status": task.status} for task in tasks]

    return Response(
        {
            "status": True,
            "message": "No tasks found." if not data else "Tasks fetched successfully.",
            "data": data
        }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_task(request, task_id):
    completion_report = request.data.get('completion_report', '').strip()
    worked_hours = request.data.get('worked_hours')
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    # Task already completed
    if task.status == Task.STATUS_COMPLETED:
        return Response(
            {
                "status": False,
                "message": "Task is already completed.",
                "data": None
            },status=status.HTTP_400_BAD_REQUEST)

    # Mandatory fields check
    if not completion_report or worked_hours is None:
        return Response(
            {
                "status": False,
                "message": "Completion report and worked hours are required.",
                "data": None
            },status=status.HTTP_400_BAD_REQUEST)

    # Update task
    task.status = Task.STATUS_COMPLETED
    task.completion_report = completion_report
    task.worked_hours = worked_hours
    task.save()

    return Response(
        {
            "status": True,
            "message": "Task marked as completed successfully.",
            "data": {
                "task_id": task.id,
                "status": task.status,
                "worked_hours": task.worked_hours
            }
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_report(request, task_id):
    """
    Admins and SuperAdmins can view completion report
    and worked hours for completed tasks only.
    """

    # Role check
    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {
                "status": False,
                "message": "You do not have permission to access this resource.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN )

    task = get_object_or_404(Task, id=task_id)

    # Business rule: only completed tasks have reports
    if task.status != Task.STATUS_COMPLETED:
        return Response(
            {
                "status": False,
                "message": "Task is not completed yet.",
                "data": None
            },status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            "status": True,
            "message": "Task completion report fetched successfully.",
            "data": {
                "task_id": task.id,
                "task_title": task.title,
                "assigned_to": task.assigned_to.username,
                "completion_report": task.completion_report,
                "worked_hours": task.worked_hours
            }
        }, status=status.HTTP_200_OK)
