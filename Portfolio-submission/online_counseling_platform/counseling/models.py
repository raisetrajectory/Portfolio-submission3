from django.db import models
from django.contrib.auth.models import User # type: ignore #2024年6月4日追加
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model() # type: ignore

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
) #6月12日追加
from django.db.models.signals import post_save #6月12日追加
from django.dispatch import receiver #6月12日追加
from uuid import uuid4 #6月12日追加
from datetime import datetime, timedelta #6月12日追加
from django.contrib.auth.models import UserManager #6月12日追加

class Users(AbstractBaseUser, PermissionsMixin): #6月12日追加
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='counseling_users_groups',  # related_name を変更
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    # AUTH_USER_MODEL = 'counseling.Users'と同じ意味です。

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='counseling_users_permissions',  # related_name を変更
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    # AUTH_USER_MODEL = 'counseling.Users'と同じ意味です。

    class Meta:
        db_table = 'users'

class UserActivateTokensManager(models.Manager): #6月12日追加

    def activate_user_by_token(self, token):
        user_activate_token = self.filter( # type: ignore
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user # type: ignore
        user.is_active =True
        user.save()

class UserActivateTokens(models.Model): #6月12日追加

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokensManager() # type: ignore

    class Meta:
        db_table = 'user_activate_tokens'

@receiver(post_save, sender=Users) #6月12日追加
def publish_token(sender, instance, **kwargs):
    print(str(uuid4()))
    print(datetime.now() + timedelta(days=1))
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1)
    )
    # メールでURLを送る方がよい
    print(f'http://127.0.0.1:8000/counseling/activate_user/{user_activate_token.token}')

class Profile(models.Model): #2024年6月4日追加
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    qualifications = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class User(AbstractUser):
    is_counselor = models.BooleanField(default=False)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='counseling_user_set',  # Changed this line
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='counseling_user_set',  # Changed this line
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneFieldの使用: CounselorモデルとUserモデルの関係性を示す場合、OneToOneFieldを使用することで、1人のユーザーが1人のカウンセラーに関連付けられることを表現できます。
    name = models.CharField(max_length=100, default='default_value_here') #カウンセラーの名前を保存するためのフィールドです。
    qualifications = models.TextField(default='default_value_here') #カウンセラーの資格や経歴など、長いテキスト情報を保存するためのフィールドです。
    bio = models.TextField() #カウンセラーの自己紹介やプロフィールを格納するためのフィールドです。

class CounselingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user: セッションを受けるユーザー（クライアント）
    counselor = models.ForeignKey('Counselor', on_delete=models.CASCADE) #2024年6月8日追加
    start_time = models.DateTimeField(auto_now_add=True) #start_time: セッションの開始時刻
    end_time = models.DateTimeField(null=True, blank=True) #end_time: セッションの終了時刻（未設定の場合もある）

    def __str__(self):
        return f'Session between {self.user.username} and {self.counselor.name}'

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.IntegerField()  # session_id フィールドを追加

    def __str__(self):
        return f'{self.sender}: {self.message}'

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

