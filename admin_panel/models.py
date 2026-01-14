from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks" )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class UserAdminMap(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_users",
        limit_choices_to={"is_staff": True, "is_superuser": False},
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_mapping",
        limit_choices_to={"is_staff": False, "is_superuser": False},
    )

    def __str__(self):
        return f"{self.user.username} → {self.admin.username}"
