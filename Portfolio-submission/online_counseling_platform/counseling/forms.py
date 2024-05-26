# counseling/forms.py
from django import forms
from .models import Counselor
from accounts.models import CustomUser # type: ignore
from django.contrib.auth.models import User

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser  # UserではなくCustomUserを使用
#         fields = ['username', 'email', 'profile_picture']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Userモデルを使用
        fields = ['username', 'email', 'profile_picture']