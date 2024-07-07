from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager,Group,Permission
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager

# class UserManager(BaseUserManager):
    #ユーザー作成手法
    # def create_user(self, username, email, password=True):
        # if not email:
            # raise ValueError('emailを入力してください')
        # user = self.model(
            # username = username,
            # email = email,
        # )
        # user.set_password(password)
        # user.save(using=self._db)
        # return user
    # def create_superuser(self, username, email, password=True):
        # user = self.model(
            # username = username,
            # email = email,
        # )
        # user.set_password(password)
        # user.is_staff = True
        # user.is_active = True
        # user.is_superuser = True
        # user.save(using=self._db)
        # return user

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')
    # introduction = models.CharField(max_length=255, null=True)
    # counselor = models.OneToOneField('boards.Counselors',on_delete=models.SET_NULL,related_name='user',null=True)#一人のユーザーが一人のカウンセラーに関連付けられます。
    # counselor = models.Foreignkey('Counselor',on_delete=models.SET_NULL,related_name='clinents',null=True, black=True)

    # groups =  models.ManyToManyField(
        # Group,
        # related_name='user_groups'
    # )
    # user_permissions = models.ManyToManyField(
        # Permission,
        # related_name='user_permissions'
    # )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # def __str__(self):
        # return self.username

    class Meta:
        db_table = 'users'

# class Counselor(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=255)
#     age = models.PositiveIntegerField(default=0, null=True)
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     picture = models.FileField(null=True, upload_to='picture/')
#     # introduction = models.CharField(max_length=255, null=True)
#     counselor = models.OneToOneField('boards.Counselors',on_delete=models.SET_NULL,related_name='user',null=True)#一人のユーザーが一人のカウンセラーに関連付けられます。
#     # counselor = models.Foreignkey('Counselors',on_delete=models.SET_NULL,related_name='clinents',null=True, black=True)
#     qualifications = models.CharField(max_length=255, null=True)

    # objects = UserManager()

    # def __str__(self):
        # return self.username

    # class Meta:
    #     db_table = 'counselor'

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

