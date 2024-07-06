from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager
from accounts.models import Users  # assuming Users model is defined in accounts.models

class ThemesManager(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()

class Themes(models.Model):

    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )

    objects = ThemesManager()

    class Meta:
        db_table = 'themes'

class CommentsManager(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

class Comments(models.Model):

    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'Themes', on_delete=models.CASCADE
    )
    objects = CommentsManager()

    class Meta:
        db_table = 'comments'

# class Counselors(models.Model):
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'counselors'

class Counselors(models.Model):
    counselorname = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')
    users = models.ManyToManyField('accounts.Users',related_name='counselors')#一人のカウンセラーが複数のユーザーと関連付けられます。

    # objects = CounselorManager()  # カスタムマネージャーを指定する

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['counselorname']

    class Meta:
        db_table = 'counselors'

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/')
