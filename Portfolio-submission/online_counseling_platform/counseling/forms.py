# counseling/forms.py
from django import forms
from .models import Counselor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 'bio'フィールドのみを含める

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(max_length=150, help_text='必須。有効なメールアドレスを入力してください。')

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
#         labels = {
#             'username': 'ユーザーネーム',
#             'email': 'メールアドレス',
#         }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='必須。有効なメールアドレスを入力してください。')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'ユーザーネーム',
            'email': 'メールアドレス',
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネームまたはメールアドレス')
