from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': "ユーザー名"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': "メールアドレス"}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "ユーザーID"}))
    about_me = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "自己紹介"}), required=False)

    class Meta:
        model = Users
        fields = ('name', 'email', 'username', 'about_me')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about_me'].required = False

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください")

        user = self.instance
        if Users.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise ValidationError("このメールアドレスは既に使用されています")

        return email



class RegistForm(forms.ModelForm):
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

class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture')

class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

class PasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Users
        fields = ('password', )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

