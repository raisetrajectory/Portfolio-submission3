# counseling/forms.py
from django import forms
from .models import Counselor
from accounts.models import CustomUser  # CustomUserをインポート

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # UserではなくCustomUserを使用
        fields = ['username', 'email', 'profile_picture']