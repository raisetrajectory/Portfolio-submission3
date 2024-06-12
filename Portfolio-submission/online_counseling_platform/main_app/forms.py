from django import forms #6月12日追加
from .models import Themes, Comments # type: ignore #6月12日追加

class CreateThemeForm(forms.ModelForm): #6月12日追加
    title = forms.CharField(label='タイトル')

    class Meta:
        model = Themes
        fields = ('title',)

class DeleteThemeForm(forms.ModelForm): #6月12日追加

    class Meta:
        model = Themes
        fields = []

class PostCommentForm(forms.ModelForm): #6月12日追加
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))

    class Meta:
        model = Comments
        fields = ('comment', )