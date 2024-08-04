# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from .models import Users, Counselor
import logging #新規追加
logger = logging.getLogger(__name__) #新規追加

User = get_user_model()

# class CustomAuthBackend(BaseBackend): #記載内容のバックアップです! 問題や不具合が発生した場合はこの記載内容に戻りましょう！
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             # Usersモデルで認証を試行
#             user = Users.objects.get(email=email)
#             if user.check_password(password): # type: ignore
#                 return user
#         except Users.DoesNotExist:
#             pass
#         except MultipleObjectsReturned:
#             # 複数のUsersオブジェクトが見つかった場合の例外処理
#             pass

#         try:
#             # Counselorモデルで認証を試行
#             counselor = Counselor.objects.get(email=email)
#             if counselor.check_password(password): # type: ignore
#                 return counselor
#         except Counselor.DoesNotExist:
#             pass
#         except MultipleObjectsReturned:
#             # 複数のCounselorオブジェクトが見つかった場合の例外処理
#             pass

#         return None

#     def get_user(self, user_id): #記載内容のバックアップです!　問題や不具合が発生した場合はこの記載内容に戻りましょう！
#         try:
#             return Users.objects.get(pk=user_id)
#         except Users.DoesNotExist:
#             try:
#                 return Counselor.objects.get(pk=user_id)
#             except Counselor.DoesNotExist:
#                 return None

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        logger.debug(f"Authenticating user with email: {email}")
        try:
            # Usersモデルで認証を試行
            user = Users.objects.get(email=email)
            if user.check_password(password): # type: ignore
                logger.debug(f"User {user} authenticated with Users model.")
                return user
        except Users.DoesNotExist:
            logger.debug("No user found in Users model.")
        except MultipleObjectsReturned:
            logger.warning("Multiple users found in Users model with the same email.")

        try:
            # Counselorモデルで認証を試行
            counselor = Counselor.objects.get(email=email)
            if counselor.check_password(password): # type: ignore
                logger.debug(f"Counselor {counselor} authenticated with Counselor model.")
                return counselor
        except Counselor.DoesNotExist:
            logger.debug("No counselor found in Counselor model.")
        except MultipleObjectsReturned:
            logger.warning("Multiple counselors found in Counselor model with the same email.")

        logger.debug("Authentication failed for all models.")
        return None

    def get_user(self, user_id):
        logger.debug(f"Fetching user with ID: {user_id}")
        try:
            user = Users.objects.get(pk=user_id)
            logger.debug(f"User found in Users model: {user}")
            return user
        except Users.DoesNotExist:
            logger.debug("No user found in Users model with the given ID.")
            try:
                counselor = Counselor.objects.get(pk=user_id)
                logger.debug(f"Counselor found in Counselor model: {counselor}")
                return counselor
            except Counselor.DoesNotExist:
                logger.debug("No counselor found in Counselor model with the given ID.")
                return None