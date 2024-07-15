from django import forms
from .models import Themes, Comments
from .models import User
from accounts.models import Users, Counselor

class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    selected_user = forms.ModelChoiceField(queryset=Users.objects.all(), label='ユーザーを選択してください')

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
