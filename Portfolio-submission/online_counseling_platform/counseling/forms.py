# counseling/forms.py
from django import forms
from .models import Counselor
from .models import User
from accounts.models import CustomUser  # CustomUserをインポート

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']