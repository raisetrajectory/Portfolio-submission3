# from django.contrib.auth import get_user_model
# from django.core.exceptions import MultipleObjectsReturned
# from .models import Users,Counselor

# User = get_user_model()

# class = CustonAuthBackend(BaseBackend):
#     def authenticate(self, requset, email=None,password=None **kwargs):
#         try:
#             Usersモデルで認証を試行
#             user = Users.objects.get(email=email)
#             if user.check_password(password):
#                 return user
#         except Users.DoesNotExist:
#             pass
#         except MultipleObjectsReturned:
#             複数のUsersオブジェクトが見つかった場合の例外処理
#             pass

#         try:
#             Counselorモデルで認証を試行
#             counselor = Counselor.objects.get(email=email)
#             if counselor.check_password(password):
#                 return counselor
#         except Counselor.DoesNotExist:
#             pass
#         except MultipleObjectsReturned:
#             複数のCounselorオブジェクトが見つかった場合の例外処理
#             pass

#         return None

# def get_user(self, user_id):
#     try:
#         return User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#     try:
#         return Counselor.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return None

# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from .models import Users, Counselor

User = get_user_model()

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Usersモデルで認証を試行
            user = Users.objects.get(email=email)
            if user.check_password(password): # type: ignore
                return user
        except Users.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            # 複数のUsersオブジェクトが見つかった場合の例外処理
            pass

        try:
            # Counselorモデルで認証を試行
            counselor = Counselor.objects.get(email=email)
            if counselor.check_password(password): # type: ignore
                return counselor
        except Counselor.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            # 複数のCounselorオブジェクトが見つかった場合の例外処理
            pass

        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            try:
                return Counselor.objects.get(pk=user_id)
            except Counselor.DoesNotExist:
                return None
