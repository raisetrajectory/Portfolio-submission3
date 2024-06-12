from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ThemesManager(models.Manager): #2024年6月12日追加

    def fetch_all_themes(self):
        return self.order_by('id').all()

class Themes(models.Model): #2024年6月12日追加

    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'counseling.Users', on_delete=models.CASCADE
    )

    objects = ThemesManager()

    class Meta:
        db_table = 'themes'

class CommentsManager(models.Manager): #2024年6月12日追加
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

# class Comments(models.Model): #2024年6月12日追加

#     comment = models.CharField(max_length=1000)
#     user = models.ForeignKey(
#         'accounts.Users', on_delete=models.CASCADE
#     )
#     theme = models.ForeignKey(
#         'Themes', on_delete=models.CASCADE
#     )
#     objects = CommentsManager()

#     class Meta:
#         db_table = 'comments'

class User(AbstractUser):
    is_counselor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='counselor_pictures/')
    bio = models.TextField(blank=True)  # Add a bio field as an example

    def __str__(self):
        return self.name

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

from .models import CounselingSession, ChatMessage

@login_required
def chat_view(request, session_id):
    session = get_object_or_404(CounselingSession, id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    return render(request, 'chat.html', {'session': session, 'messages': messages})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        message = request.POST.get('message')
        session = get_object_or_404(CounselingSession, id=session_id)
        ChatMessage.objects.create(session=session, sender=request.user, message=message)
        return JsonResponse({'status': 'success'})
