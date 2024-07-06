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
    # objects = UserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['counselorname']

    class Meta:
        db_table = 'counselors'

# class UserActivateTokensManager(models.Manager):

#     def activate_user_by_token(self, token):
#         user_activate_token = self.filter( # type: ignore
#             token=token,
#             expired_at__gte=datetime.now()
#         ).first()
#         user = user_activate_token.user # type: ignore
#         user.is_active =True
#         user.save()

# class UserActivateTokens(models.Model):

#     token = models.UUIDField(db_index=True)
#     expired_at = models.DateTimeField()
#     user = models.ForeignKey(
#         'Users', on_delete=models.CASCADE
#     )

#     objects = UserActivateTokensManager() # type: ignore

#     class Meta:
#         db_table = 'user_activate_tokens'

# @receiver(post_save, sender=Users)
# def publish_token(sender, instance, **kwargs):
#     print(str(uuid4()))
#     print(datetime.now() + timedelta(days=1))
#     user_activate_token = UserActivateTokens.objects.create(
#         user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1)
#     )
#     # メールでURLを送る方がよい
#     print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')


class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/')
