from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD) # type: ignore
        if username is None or password is None:
            return
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

# class EmailOrUsernameModelBackend(ModelBackend): #6月追加
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if username is None:
#             username = kwargs.get(UserModel.USERNAME_FIELD)
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user