from django import forms
from .models import Themes, Comments
from .models import User

class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')

    class Meta:
        model = Themes
        fields = ('title',)

class DeleteThemeForm(forms.ModelForm):

    class Meta:
        model = Themes
        fields = []

class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))

    class Meta:
        model = Comments
        fields = ('comment', )

class UserInfo(forms.Form): #不要の場合は削除して大丈夫です！
    name = forms.CharField()
    age = forms.IntegerField()
    mail = forms.EmailField()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

from .models import Counselors
from django.contrib.auth.password_validation import validate_password

class CounselorRegistForm(forms.ModelForm):
    counselorname = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = Counselors
        fields = ('counselorname', 'age', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

#     def save(self, commit=False):
#         counselor =super().save(commit=False)
#         validate_password(self.cleaned_data['password'], counselor)
#         counselor.set_password(self.cleaned_data['password'])
#         counselor.save()
#         return counselor

# class CounselorEditForm(forms.ModelForm):
#     username = forms.CharField(label='ユーザーネーム')
#     age = forms.IntegerField(label='年齢', min_value=0)
#     email = forms.EmailField(label='メールアドレス')
#     picture = forms.FileField(label='写真', required=False)

#     class Meta:
#         model = Counselors
#         fields = ('username', 'age', 'email', 'picture')