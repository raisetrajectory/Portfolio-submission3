from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_counselor = models.BooleanField(default=False)

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    # Add other fields relevant to counselors

class CounselingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    # Add other fields relevant to sessions

class ChatMessage(models.Model):
    session = models.ForeignKey(CounselingSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    ASSIGNED_ROLE_CHOICES = [
        ('user', 'User'),
        ('counselor', 'Counselor'),
    ]

    assigned_id = models.IntegerField()
    assigned_role = models.CharField(max_length=10, choices=ASSIGNED_ROLE_CHOICES)
    task_name = models.CharField(max_length=255)
    task_type = models.CharField(max_length=50)
    complete_flg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
