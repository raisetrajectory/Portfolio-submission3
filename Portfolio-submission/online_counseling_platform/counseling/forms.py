# counseling/forms.py
from django import forms
from .models import Counselor, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import Themes, Comments # type: ignore

class UploadFileForm(forms.Form): #2024年6月6日追加
    upload_file = forms.ImageField(label='画像ファイルを選択してください')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 'bio'フィールドのみを含める

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

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

class ChatMessageForm(forms.ModelForm): #2024年6月11日追加　記載内容のバックアップです。　
    session_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ChatMessage
        fields = ['message', 'session_id']

class CommentForm(forms.Form):
    message = forms.CharField(label='コメント', widget=forms.Textarea)