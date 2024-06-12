# counseling/forms.py
from django import forms
from .models import Counselor, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Users #6月12日追加
from django.contrib.auth.password_validation import validate_password #6月12日追加

class RegistForm(forms.ModelForm): #6月12日追加
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = ('username', 'age', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user =super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class UserEditForm(forms.ModelForm): #6月12日追加
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture')

# class PasswordChangeForm(forms.ModelForm): #6月12日追加

#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
#     confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

#     class Meta():
#         model = Users
#         fields = ('password', )

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data['password']
#         confirm_password = cleaned_data['confirm_password']
#         if password != confirm_password:
#             raise forms.ValidationError('パスワードが異なります')

#     def save(self, commit=False):
#         user = super().save(commit=False)
#         validate_password(self.cleaned_data['password'], user)
#         user.set_password(self.cleaned_data['password'])
#         user.save()
#         return user

class LoginForm(forms.Form): #6月12日追加
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

# class PasswordChangeForm(forms.ModelForm): #6月12日追加

#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
#     confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

#     class Meta():
#         model = Users
#         fields = ('password', )

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data['password']
#         confirm_password = cleaned_data['confirm_password']
#         if password != confirm_password:
#             raise forms.ValidationError('パスワードが異なります')

#     def save(self, commit=False):
#         user = super().save(commit=False)
#         validate_password(self.cleaned_data['password'], user)
#         user.set_password(self.cleaned_data['password'])
#         user.save()
#         return user


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