from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager

# class Counselor(models.Model):
#     counselorname = models.CharField(max_length=255)
#     age = models.PositiveIntegerField()
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     picture = models.FileField(null=True, upload_to='picture/')

#     objects = models.Manager()
#     objects = UserManager()

#     COUNSELORNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['counselorname']

#     class Meta:
#         db_table = 'accounts.counselors'

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')
    counselor = models.OneToOneField('boards.Counselors',on_delete=models.SET_NULL,related_name='user',null=True)#一人のユーザーが一人のカウンセラーに関連付けられます。

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter( # type: ignore
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user # type: ignore
        user.is_active =True
        user.save()

class UserActivateTokens(models.Model):

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )

    objects = UserActivateTokensManager() # type: ignore

    class Meta:
        db_table = 'user_activate_tokens'

@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    print(str(uuid4()))
    print(datetime.now() + timedelta(days=1))
    user_activate_token = UserActivateTokens.objects.create(
        user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1)
    )
    # メールでURLを送る方がよい
    print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')

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
