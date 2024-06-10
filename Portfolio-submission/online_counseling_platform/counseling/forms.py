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
from .models import Counselor, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms #2024年6月5日追加
# from .models import Profile # type: ignore #2024年6月5日追加

# class UploadFileForm(forms.Form): #2024年6月6日追加
#     upload_file = forms.ImageField()

class UploadFileForm(forms.Form): #2024年6月6日追加
    upload_file = forms.ImageField(label='画像ファイルを選択してください')

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 'bio'フィールドのみを含める

# from .models import Profile #2024年6月4日追加

# class ProfileForm(forms.ModelForm):  #2024年6月4日追加 # type: ignore
#     class Meta:
#         model = Profile
#         fields = ['bio', 'profile_picture']

class CounselorForm(forms.ModelForm):
    class Meta:
        model = Counselor
        fields = ['bio']  # 他の必要なフィールドを追加

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Counselor
#         fields = ['bio']  # 'bio'フィールドのみを含める

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

# class ChatMessageForm(forms.ModelForm): #記載内容のバックアップです。ここに戻りましょう！
#     session_id = forms.CharField(widget=forms.HiddenInput(), required=True)

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

# class ChatMessageForm(forms.ModelForm):　#2024年6月10日追加
#     # セッションIDのフィールドを追加
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']  # 'session_id' フィールドを追加

# class ChatMessageForm(forms.ModelForm): #2024年6月9日追加
#     session_id = forms.CharField(widget=forms.HiddenInput(), required=True)

#     class Meta:
#         model = ChatMessage
#         fields = ['message']

# class ChatMessageForm(forms.ModelForm): #2024年6月10日追加
#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']  # 'session_id' フィールドを追加

#     session_id = forms.IntegerField(widget=forms.HiddenInput())  # HiddenInput を使用して非表示にする

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session']  # session フィールドを追加

# class ChatMessageForm(forms.ModelForm): #2024年6月10日追加
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

#     def __init__(self, *args, session_id=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['session_id'].initial = session_id
#         self.fields['session_id'].widget = forms.HiddenInput()

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message']

#     def __init__(self, *args, session_id=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.session_id = session_id

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if self.session_id:
#             instance.session_id = self.session_id
#         if commit:
#             instance.sender = self.request.user  # type: ignore # ここで sender に request.user をセット
#             instance.save()
#         return instance

# class ChatMessageForm(forms.ModelForm):
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

#     def __init__(self, *args, session_id=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         if session_id:
#             self.fields['session_id'].initial = session_id

# class ChatMessageForm(forms.ModelForm):
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

#     def __init__(self, *args, session_id=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         if session_id:
#             self.fields['session_id'].initial = session_id

# class ChatMessageForm(forms.ModelForm):
#     session_id = forms.IntegerField(widget=forms.HiddenInput())

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

#     def __init__(self, *args, session_id=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         if session_id:
#             self.fields['session_id'].initial = session_id
#         else:
#             self.fields['session_id'].initial = 0  # デフォルト値を設定

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message', 'session_id']
        widgets = {
            'session_id': forms.HiddenInput()
        }



# class ChatMessageForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         session_id = kwargs.pop('session_id', None)
#         super(ChatMessageForm, self).__init__(*args, **kwargs)
#         if session_id is not None:
#             self.fields['session_id'].initial = session_id
#             self.fields['session_id'].widget = forms.HiddenInput()

#     class Meta:
#         model = ChatMessage
#         fields = ['message', 'session_id']

class CommentForm(forms.Form):
    message = forms.CharField(label='コメント', widget=forms.Textarea)