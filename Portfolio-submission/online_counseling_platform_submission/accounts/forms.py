from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from .models import Counselor

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

class CounselorRegistForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta:
        model = Counselor
        fields = ('username', 'age', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=True):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)
    picture2 = forms.ImageField(label='新しい写真', required=False)
    introduction = forms.CharField(label='自己紹介', required=False, widget=forms.Textarea)
    counselor = forms.ModelChoiceField(queryset=Counselor.objects.all(), required=False, label='カウンセラー') #ユーザーはフォームでカウンセラーを選択できるようになりますが、必須ではないため、選択しなくてもフォームを提出できます。

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture', 'picture2', 'introduction', 'counselor')

class CounselorEditForm(forms.ModelForm):
    username = forms.CharField(label='ユーザーネーム')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)
    picture2 = forms.ImageField(label='新しい写真', required=False)  # 新しい ImageField を追加します！
    introduction = forms.CharField(label='自己紹介', required=False, widget=forms.Textarea)
    qualifications = forms.CharField(label='資格', required=False)

    class Meta:
        model = Counselor
        fields = ('username', 'age', 'email', 'picture', 'picture2', 'introduction', 'qualifications')


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

