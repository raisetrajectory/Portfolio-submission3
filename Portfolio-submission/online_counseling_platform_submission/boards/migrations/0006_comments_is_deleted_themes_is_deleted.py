# Generated by Django 4.2.11 on 2024-08-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("boards", "0005_alter_comments_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="themes",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
