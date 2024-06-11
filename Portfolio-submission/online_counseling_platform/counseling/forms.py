# counseling/forms.py
from django import forms
from .models import Counselor, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import Themes, Comments  #2024年6月12日追加

# class CreateThemeForm(forms.ModelForm): #2024年6月12日追加
#     title = forms.CharField(label='タイトル')

#     class Meta:
#         model = Themes
#         fields = ('title',)


# class DeleteThemeForm(forms.ModelForm):#2024年6月12日追加

#     class Meta:
#         model = Themes
#         fields = []

# class PostCommentForm(forms.ModelForm):#2024年6月12日追加
#     comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))

#     class Meta:
#         model = Comments
#         fields = ('comment', )

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