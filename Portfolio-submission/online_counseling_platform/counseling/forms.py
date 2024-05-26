# counseling/forms.py
from django import forms
from .models import Counselor
from django.contrib.auth.models import User

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 'bio'フィールドのみを含める