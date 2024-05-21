# counseling/forms.py
from django import forms
from .models import Counselor

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加
