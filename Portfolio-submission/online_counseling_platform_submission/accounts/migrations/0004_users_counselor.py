# Generated by Django 4.2.11 on 2024-07-06 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("boards", "0004_rename_name_counselors_counselorname_and_more"),
        ("accounts", "0003_alter_users_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="counselor",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user",
                to="boards.counselors",
            ),
        ),
    ]
