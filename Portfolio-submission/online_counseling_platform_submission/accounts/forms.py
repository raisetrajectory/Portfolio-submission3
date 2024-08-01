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

class CounselorRegistForm(RegistForm):
    username = forms.CharField(label='カウンセラーネーム')

    class Meta(RegistForm.Meta):
        model = Counselor
        fields = ('username', 'age', 'email', 'password')

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
    username = forms.CharField(label='カウンセラーネーム')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)
    picture2 = forms.ImageField(label='新しい写真', required=False)
    introduction = forms.CharField(label='自己紹介', required=False, widget=forms.Textarea)
    qualifications = forms.CharField(label='資格', required=False)
    is_counselor = forms.BooleanField(label='カウンセラーとしてログイン中', required=False)

    class Meta:
        model = Counselor
        fields = ('username', 'age', 'email', 'picture', 'picture2', 'introduction', 'qualifications', 'is_counselor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # インスタンスが存在する場合は、その値を初期値として設定する
            self.fields['is_counselor'].initial = instance.user.is_counselor if hasattr(instance, 'user') else False
        # is_counselor フィールドを無効化しない
        if 'is_counselor' in self.fields:
            self.fields['is_counselor'].disabled = False

    def save(self, commit=True):
        # フォームが保存された後にインスタンスを再初期化する
        instance = super().save(commit=False)
        # インスタンスのuser属性のis_counselorフィールドを更新
        if hasattr(instance, 'user'):
            instance.user.is_counselor = self.cleaned_data['is_counselor']
            instance.user.save()
        if commit:
            instance.save()

        # 保存後のインスタンスの値を反映してフォームを再初期化する
        instance.refresh_from_db()  # インスタンスをデータベースから最新の情報でリフレッシュ
        self.initial['is_counselor'] = instance.user.is_counselor if hasattr(instance, 'user') else False
        self.fields['is_counselor'].initial = instance.user.is_counselor if hasattr(instance, 'user') else False

        return instance

class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

class CounselorLoginForm(forms.Form):
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

class CounselorPasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='新しいパスワード再入力', widget=forms.PasswordInput())

    class Meta:
        model = Counselor
        fields = ('password', )

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