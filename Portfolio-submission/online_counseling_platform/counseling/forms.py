# counseling/forms.py
from django import forms
from .models import Counselor
from django.contrib.auth.models import User

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = User  # Userモデルを使用
#         fields = ['username', 'email', 'profile_picture']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Counselor  # Counselor モデルを使用する
#         fields = ['bio', 'profile_picture']  # プロフィール情報に対応するフィールドを追加

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Counselor
#         fields = ['picture']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['name', 'age', 'grade', 'profile_picture']  # profile_pictureを含める