# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     is_counselor = models.BooleanField(default=False)

#     # Add related_name to avoid clashes
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='counseling_user_set',  # Changed this line
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='counseling_user_set',  # Changed this line
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

# class Counselor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField()

# class CounselingSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField(null=True, blank=True)

# class ChatMessage(models.Model):
#     session = models.ForeignKey(CounselingSession, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# class Task(models.Model):
#     ASSIGNED_ROLE_CHOICES = [
#         ('user', 'User'),
#         ('counselor', 'Counselor'),
#     ]

#     assigned_id = models.IntegerField()
#     assigned_role = models.CharField(max_length=10, choices=ASSIGNED_ROLE_CHOICES)
#     task_name = models.CharField(max_length=255)
#     task_type = models.CharField(max_length=50)
#     complete_flg = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# 1~51の記載内容に関しては、現段階で問題無い記載となっております。バックアップ保存用です！

from django.db import models
from django.contrib.auth.models import User # type: ignore #2024年6月4日追加
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model() # type: ignore

# class Profile(models.Model): #2024年6月4日追加
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
#     name = models.CharField(max_length=100, null=True, blank=True)
#     bio = models.TextField(null=True, blank=True)
#     qualifications = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return self.user.username

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
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE) #counselor: セッションを行うカウンセラー
    start_time = models.DateTimeField(auto_now_add=True) #start_time: セッションの開始時刻
    end_time = models.DateTimeField(null=True, blank=True) #end_time: セッションの終了時刻（未設定の場合もある）

# class ChatMessage(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     session = models.ForeignKey(CounselingSession, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.sender.username}: {self.message}'

#     def delete_message(self):
#         self.delete()

class ChatMessage(models.Model):
    session = models.ForeignKey(CounselingSession, on_delete=models.CASCADE) #メッセージが関連付けられているカウンセリングセッションを示します。
    sender = models.ForeignKey(User, on_delete=models.CASCADE) #メッセージを送信したユーザーを示します。
    message = models.TextField() #チャットメッセージの本文を保持します。TextFieldは長文テキストを保存するためのフィールドで、メッセージの内容がここに保存されます。
    timestamp = models.DateTimeField(auto_now_add=True) #timestampは、メッセージが送信された日時を記録します。

    def __str__(self):
        return f'{self.sender.username}: {self.message}'

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

# 55~129の記載内容に関しては、現段階で問題無い記載となっております。バックアップ保存用です！
