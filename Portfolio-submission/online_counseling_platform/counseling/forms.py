# counseling/forms.py
from django import forms
from .models import Counselor
# from .models import Counselor, ChatMessage  # ChatMessage を追加
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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='必須。有効なメールアドレスを入力してください。')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'ユーザーネーム',
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='ユーザーネームまたはメールアドレス')

# class ChatMessageForm(forms.ModelForm):  # ChatMessageForm を追加
#     class Meta:
#         model = ChatMessage
#         fields = ['content']