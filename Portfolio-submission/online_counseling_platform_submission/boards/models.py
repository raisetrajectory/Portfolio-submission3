from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager

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

class Counselors(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'counselors'

# class Counselors(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(max_length=255)
#     age = models.PositiveIntegerField()
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     picture = models.FileField(null=True, upload_to='picture/')
    # user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    
#     objects = models.Manager()
    # objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     class Meta:
#         db_table = 'counselors'

# class CounselorActivateTokensManager(models.Manager):

#     def activate_counselor_by_token(self, token):
#         counselor_activate_token = self.filter(
#             token=token,
#             expired_at__gte=datetime.now()
#         ).first()
#         if counselor_activate_token:
#             counselor = counselor_activate_token.counselor
#             counselor.is_active = True
#             counselor.save()

# class CounselorActivateTokens(models.Model):
#     token = models.UUIDField(db_index=True)
#     expired_at = models.DateTimeField()
#     counselor = models.ForeignKey(
#         'Counselors', on_delete=models.CASCADE
#     )

#     objects = CounselorActivateTokensManager() # type: ignore

#     class Meta:
#         db_table = 'counselor_activate_tokens'

# @receiver(post_save, sender=Counselors)
# def publish_counselor_token(sender, instance, **kwargs):
#     if kwargs.get('created', False):  # 新規作成されたときのみトークンを発行
#         token = str(uuid4())
#         expired_at = datetime.now() + timedelta(days=1)
#         counselor_activate_token = CounselorActivateTokens.objects.create(
#             counselor=instance, token=token, expired_at=expired_at
#         )
#         # メールでURLを送る方がよい
#         print(f'http://127.0.0.1:8000/accounts/activate_counselor/{counselor_activate_token.token}')

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/')
