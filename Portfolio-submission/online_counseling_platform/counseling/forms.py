# # counseling/forms.py
# from django import forms
# from .models import Counselor
# from .models import Counselor, ChatMessage  # ChatMessage を追加
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# class CounselorForm(forms.ModelForm):
#     class Meta:
#         model = Counselor
#         fields = ['bio']  # 他の必要なフィールドを追加

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Counselor
#         fields = ['bio']  # 'bio'フィールドのみを含める

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(max_length=150, help_text='必須。有効なメールアドレスを入力してください。')

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
#         labels = {
#             'username': 'ユーザーネーム',
#         }

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(label='ユーザーネームまたはメールアドレス')

# class ChatMessageForm(forms.ModelForm):  # ChatMessageForm を追加
#     class Meta:
#         model = ChatMessage
#         fields = ['message']
#         labels = {
#             'message': 'メッセージ',
#         }

# 1~37の記載内容に関しては、現段階で問題無い記載となっております。バックアップ保存用です！

# counseling/forms.py
from django import forms
from .models import Counselor
from .models import Counselor, ChatMessage  # ChatMessage を追加
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

# class ChatMessageForm(forms.ModelForm):
#     session_id = forms.IntegerField(widget=forms.HiddenInput())  # session_id を追加

#     class Meta:
#         model = ChatMessage
#         fields = ['session_id', 'message']  # session_id を含める
#         labels = {
#             'message': 'メッセージ',
#         }

# class ChatMessageForm(forms.ModelForm):
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']
#         labels = {
#             'message': 'メッセージ',
#         }

class ChatMessageForm(forms.ModelForm):
    session_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = ChatMessage
        fields = ['message', 'session_id']

class CommentForm(forms.Form):
    message = forms.CharField(label='コメント', widget=forms.Textarea)