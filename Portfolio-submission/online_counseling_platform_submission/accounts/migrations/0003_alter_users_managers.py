# Generated by Django 4.2.11 on 2024-06-17 07:46

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_useractivatetokens"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="users",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]