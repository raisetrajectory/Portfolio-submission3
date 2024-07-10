from django.db import models
from accounts.models import Counselor  # accountsアプリのCounselorモデルをインポート #記載内容の追加です!

class ThemesManager(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()

class Themes(models.Model):

    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    counselor = models.ForeignKey(
        Counselor, on_delete=models.CASCADE, related_name='themes', null=True, blank=True
    )  # Counselorモデルを関連付ける #記載内容の追加です!

    objects = ThemesManager()

    class Meta:
        db_table = 'themes'

class CommentsManager(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()

class Comments(models.Model):

    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'Themes', on_delete=models.CASCADE
    )
    counselor = models.ForeignKey(
        Counselor, on_delete=models.CASCADE, related_name='comments', null=True, blank=True
    )  # Counselorモデルを関連付ける #記載内容の追加です!

    objects = CommentsManager()

    class Meta:
        db_table = 'comments'

class Counselors(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'counselors'

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/')
